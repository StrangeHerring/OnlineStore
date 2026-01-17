from abc import ABC, abstractmethod


class AbstractRemoveMyAccountUseCase(ABC):
    @abstractmethod
    async def execute(self, token):
        ...