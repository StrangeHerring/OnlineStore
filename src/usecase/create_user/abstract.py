from abc import ABC, abstractmethod

from api.v1.user.models import UserCreate


class AbstractCreateUserUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: UserCreate):
        ...