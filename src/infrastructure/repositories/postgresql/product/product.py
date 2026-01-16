from sqlalchemy.ext.asyncio import Asyncsession
from sqlalchemy import select


from infrastructure.databases.postgresql.models.product import Product
from infrastructure.databases.postgresql.models.category import Category
from infrastructure.repositories.postgresql.category.exceptions import CategoryNotFound
from .exeptions import ProductNotFound
from src.api.v1.product.models import ProductBase, ProductCreate, ProductUpdate


class PostgreSQLProductRepository:
    def __init__(self, session: Asyncsession):
        self._session: Asyncsession = session
    
    async def get_product(self, id: int) -> ProductBase | None:
        query = select(Product).where(Product.id == id)
        result = await self._session.execute(query)
        product = result.scalar_one_or_none()
        return product
    
    async def list_products(self, limit: int, offset: int) -> list[ProductBase]:
        query = select(Product).limit(limit).offset(offset)
        result = await self._session.execute(query)
        products = result.scalars().all()
        return products
    
    async def create_product(self, payload: ProductCreate) -> ProductBase:
        category_exists = select(Category).where(Category.id == payload.category_id)
        if not category_exists:
            raise CategoryNotFound()

        product = payload.model_dump()
        self._session.add(Product(**product))

        await self._session.flush()

        schema = ProductCreate(
            id=product.id,
            title=product.title,
            description=product.description,
            price=product.price,
            discount_percentage=product.validate_discount_percentage(product.discount_percentage),
            rating=product.rating,
            stock=product.stock,
            brand=product.brand,
            thumbnail=product.thumbnail,
            images=product.images,
            is_published=product.is_published,
            created_at=product.created_at,
            category_id=product.category_id,
            category=product.category,
        )
        return schema

    async def update_product(self, id: int, payload: ProductUpdate) -> None:
        query = select(Product).where(Product.id == id)
        result = await self._session.execute(query)
        product = result.scalar_one_or_none()

        if product is None:
            raise ProductNotFound()

        product.title = payload.title
        product.description = payload.description
        product.price = payload.price
        product.discount_percentage = payload.discount_percentage
        product.rating = payload.rating
        product.stock = payload.stock
        product.brand = payload.brand
        product.thumbnail = payload.thumbnail
        product.images = payload.images
        product.is_published = payload.is_published
        product.category_id = payload.category_id

        await self._session.flush()

        return
    
    async def delete_product(self, id: int) -> None:
        query = select(Product).where(Product.id == id)
        result = await self._session.execute(query)
        product = result.scalar_one_or_none()

        if product is None:
            raise ProductNotFound()

        self._session.delete(product)
        await self._session.flush()

        return