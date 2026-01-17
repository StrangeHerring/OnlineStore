from abc import ABC, abstractmethod


class AbstractGetMyInfoUseCase(ABC):
    @abstractmethod
    async def execute(self, token):
        ...