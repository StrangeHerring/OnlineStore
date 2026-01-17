from abc import ABC, abstractmethod


class AbstractRefreshTokenUseCase(ABC):
    @abstractmethod
    async def execute(self, token):
        ...