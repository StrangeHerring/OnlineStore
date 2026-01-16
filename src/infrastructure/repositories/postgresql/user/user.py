import re

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.user.models import UserBase, UserCreate, UserUpdate
from infrastructure.databases.postgresql.models.user import User
from src.api.v1.user.exceptions import UserIsExist, UserNotFound
from src.api.v1.security import get_password_hash


class PostgreSQLUserRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session
    
    async def create_user(self, payload: UserCreate) -> UserBase:
        hashed_password = get_password_hash(payload.password)
        user = User(
            full_name=payload.full_name,
            username=payload.username,
            password=hashed_password,
            email=payload.email,
        )
        self._session.add(user)
    
        try:
            await self._session.flush()
        except IntegrityError as e:
            pattern = r'Key \((.*?)\)=\((.*?)\)'
            match = re.search(pattern, str(e))
            columns = [col.strip() for col in match.group(1).split(',')]
            values = [val.strip() for val in match.group(2).split(',')]

            raise UserIsExist(field=columns[0], value=values[0])
        
        schema = UserCreate(
            id=user.id,
            full_name=user.full_name,
            username=user.username,
            email=user.email,
        )
        return schema
    
    async def get_user(self, id: int) -> UserBase | None:
        query = select(User).where(User.id == id)
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()
        return user
    
    async def list_users(self, limit: int, offset: int) -> list[UserBase]:
        query = select(User).limit(limit).offset(offset)
        result = await self._session.execute(query)
        users = result.scalars().all()
        return users
    
    async def update_user(self, user_id: int, payload: UserUpdate) -> None:
        query = select(User).where(User.id == user_id)
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            raise UserNotFound()

        user.full_name = payload.full_name
        user.email = payload.email
        user.username = payload.username

        try:
            await self._session.flush()
        except IntegrityError as e:
            pattern = r'Key \((.*?)\)=\((.*?)\)'
            match = re.search(pattern, str(e))
            columns = [col.strip() for col in match.group(1).split(',')]
            values = [val.strip() for val in match.group(2).split(',')]

            raise UserIsExist(field=columns[0], value=values[0])
        
        return
    
    async def delete_user(self, user_id: int) -> None:
        query = select(User).where(User.id == user_id)
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            raise UserNotFound()

        self._session.delete(user)
        await self._session.flush()

        return