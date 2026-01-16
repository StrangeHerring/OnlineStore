from sqlalchemy.ext.asyncio import Asyncsession
from sqlalchemy import select


from infrastructure.databases.postgresql.models.category import Category
from infrastructure.repositories.postgresql.category.exceptions import CategoryNotFound
from src.api.v1.category.models import CategoryBase, CategoryCreate, CategoryUpdate


class PostgreSQLCategoryRepository:
    def __init__(self, session: Asyncsession):
        self._session: Asyncsession = session
    
    async def get_category(self, id: int) -> CategoryBase | None:
        query = select(Category).where(Category.id == id)
        result = await self._session.execute(query)
        category = result.scalar_one_or_none()
        return category
    
    async def list_categories(self, limit: int, offset: int) -> list[CategoryBase]:
        query = select(Category).limit(limit).offset(offset)
        result = await self._session.execute(query)
        categories = result.scalars().all()
        return categories
    
    async def create_category(self, payload: CategoryCreate) -> CategoryBase:
        category = payload.model_dump()
        self._session.add(Category(**category))

        await self._session.flush()

        schema = CategoryCreate(
            id=category.id,
            name=category.name
        )
        return schema

    async def update_category(self, id: int, payload: CategoryUpdate) -> None:
        query = select(Category).where(Category.id == id)
        result = await self._session.execute(query)
        category = result.scalar_one_or_none()

        if category is None:
            raise CategoryNotFound()

        category.name = payload.name

        await self._session.flush()

        return
    
    async def delete_category(self, id: int) -> None:
        query = select(Category).where(Category.id == id)
        result = await self._session.execute(query)
        category = result.scalar_one_or_none()

        if category is None:
            raise CategoryNotFound()

        self._session.delete(category)
        await self._session.flush()

        return