import re

from fastapi import HTTPException, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from infrastructure.databases.postgresql.session import get_async_session

from infrastructure.databases.postgresql.models.user import User
from infrastructure.repositories.postgresql.user.exceptions import UserIsExist
from src.api.v1.security import verify_password, get_user_token, get_token_payload, get_password_hash
from src.api.v1.auth.models import Signup, TokenResponse



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class PostgreSQLAuthRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self._session = session
    
    async def login(self, credentials: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
        query = select(User).where(User.username == credentials.username)
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Incorrect username or password",
            )

        if not verify_password(credentials.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Incorrect username or password",
            )

        return await get_user_token(id=user.id)
    
    async def signup(self, payload: Signup) -> None:
        hashed_password = get_password_hash(payload.password)
        payload.password = hashed_password
        self._session.add(User(id=None,**payload.model_dump()))

        try:
            await self._session.flush()
        except IntegrityError as e:
            pattern = r'Key \((.*?)\)=\((.*?)\)'
            match = re.search(pattern, str(e))
            columns = [col.strip() for col in match.group(1).split(',')]
            values = [val.strip() for val in match.group(2).split(',')]

            raise UserIsExist(field=columns[0], value=values[0])
        
        return
    
    async def get_refresh_token(self, token) -> TokenResponse:
        payload = get_token_payload(token)
        user_id = payload.get('id', None)
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        
        query = select(User).where(User.id == user_id)
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

        return await get_user_token(id=user_id)
