from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from app.domain.model import DailyFunFact


class DailyFunFactCachePort(ABC):

    @abstractmethod
    async def store(self, fun_fact: DailyFunFact) -> None:
        pass

    @abstractmethod
    async def get(self, date: date) -> Optional[DailyFunFact]:
        pass

    @abstractmethod
    async def get_last_n(self, limit: int) -> list[DailyFunFact]:
        pass

    @abstractmethod
    async def acquire_lock(self, date: date, ttl: int = 10) -> bool:
        pass

    @abstractmethod
    async def release_lock(self, date: date):
        pass
