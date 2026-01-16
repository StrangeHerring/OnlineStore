from abc import ABC, abstractmethod

from api.v1.category.models import CategoryCreate


class AbstractCreateCategoryUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: CategoryCreate):
        ...