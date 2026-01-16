from api.v1.category.models import CategoryCreate
from .abstract import AbstractCreateCategoryUseCase


class PostgreSQLCreateCategoryUseCase(AbstractCreateCategoryUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, schema: CategoryCreate):
        async with self._uow as uow_:
            category = await uow_.repository.create_category(schema)

        return category