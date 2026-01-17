from fastapi.security.http import HTTPAuthorizationCredentials
from passlib.context import CryptContext
from datetime import datetime, timedelta
from api.v1.config import settings
from jose import JWTError, jwt
from api.v1.auth.models import TokenResponse
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, Depends, status
from infrastructure.databases.postgresql.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security import HTTPBearer
from infrastructure.databases.postgresql.session import get_async_session
from infrastructure.utils.responses import ResponseHandler


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth_scheme = HTTPBearer()

# Create Hash Password


def get_password_hash(password):
    return pwd_context.hash(password)


# Verify Hash Password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Create Access & Refresh Token
async def get_user_token(id: int, refresh_token=None):
    payload = {"id": id}

    access_token_expiry = timedelta(minutes=settings.access_token_expire_minutes)

    access_token = await create_access_token(payload, access_token_expiry)

    if not refresh_token:
        refresh_token = await create_refresh_token(payload)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_token_expiry.seconds
    )


# Create Access Token
async def create_access_token(data: dict, access_token_expiry=None):
    payload = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    payload.update({"exp": expire})

    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


# Create Refresh Token
async def create_refresh_token(data):
    return jwt.encode(data, settings.secret_key, settings.algorithm)


# Get Payload Of Token
def get_token_payload(token):
    try:
        return jwt.decode(token, settings.secret_key, [settings.algorithm])
    except JWTError:
        raise ResponseHandler.invalid_token('access')


def get_current_user(token):
    user = get_token_payload(token.credentials)
    return user.get('id')


async def check_admin_role(
        token: HTTPAuthorizationCredentials = Depends(auth_scheme),
        session: AsyncSession = Depends(get_async_session),) -> None:
    user = get_token_payload(token.credentials)
    user_id = user.get('id')
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    role_user = result.scalar_one_or_none()
    if role_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin role required")