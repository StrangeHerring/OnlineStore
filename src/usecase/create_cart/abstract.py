from abc import ABC, abstractmethod

from api.v1.cart.models import CartCreate


class AbstractCreateCartUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: CartCreate):
        ...