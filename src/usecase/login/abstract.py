from abc import ABC, abstractmethod

from fastapi.security import OAuth2PasswordRequestForm


class AbstractLoginUseCase(ABC):
    @abstractmethod
    async def execute(self, credentials: OAuth2PasswordRequestForm):
        ...