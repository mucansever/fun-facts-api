from abc import ABC, abstractmethod


class LlmPort(ABC):

    @abstractmethod
    async def chat(self, prompt: str) -> str:
        pass
