from abc import ABC, abstractmethod

from api.v1.auth.models import Signup


class AbstractSignupUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: Signup):
        ...