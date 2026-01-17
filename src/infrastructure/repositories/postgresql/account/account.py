import re

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from infrastructure.databases.postgresql.models import User
from infrastructure.repositories.postgresql.user.exceptions import UserNotFound, UserIsExist
from src.api.v1.security import get_password_hash, get_token_payload
from src.api.v1.user.models import UserBase
from src.api.v1.account.models import AccountUpdate


class PostgreSQLAccountRepository:
    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def get_my_info(self, token) -> UserBase:
        user_id = get_token_payload(token.credentials).get('id')
        query = select(User).where(User.id == user_id)
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            raise UserNotFound()
        
        return user
    
    async def edit_my_info(self, token, updated_user: AccountUpdate) -> None:
        user_id = get_token_payload(token.credentials).get('id')
        query = select(User).where(User.id == user_id)
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            raise UserNotFound()
        
        for key, value in updated_user.model_dump().items():
            setattr(user, key, value)

        try:
            await self._session.flush()
        except IntegrityError as e:
            pattern = r'Key \((.*?)\)=\((.*?)\)'
            match = re.search(pattern, str(e))
            columns = [col.strip() for col in match.group(1).split(',')]
            values = [val.strip() for val in match.group(2).split(',')]

            raise UserIsExist(field=columns[0], value=values[0])
        
        return
    
    async def remove_my_account(self, token) -> None:
        user_id = get_token_payload(token.credentials).get('id')
        query = select(User).where(User.id == user_id)
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            raise UserNotFound()
        
        self._session.delete(user)
        await self._session.flush()

        return

        