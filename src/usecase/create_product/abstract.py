from abc import ABC, abstractmethod

from api.v1.product.models import ProductCreate


class AbstractCreateProductUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: ProductCreate):
        ...