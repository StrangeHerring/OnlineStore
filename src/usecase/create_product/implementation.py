from api.v1.product.models import ProductCreate
from .abstract import AbstractCreateProductUseCase


class PostgreSQLCreateProductUseCase(AbstractCreateProductUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, schema: ProductCreate):
        async with self._uow as uow_:
            product = await uow_.repository.create_product(schema)

        return product