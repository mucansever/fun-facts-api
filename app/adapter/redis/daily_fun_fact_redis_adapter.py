from typing import Optional
from datetime import date

import redis.asyncio as redis

from app.domain.model import DailyFunFact
from app.domain.port import DailyFunFactCachePort


class FunFactRedisAdapter(DailyFunFactCachePort):

    KEY = "funfacts"
    _LOCK_KEY_PREFIX = "funfacts:lock:"

    def __init__(self, redis_url: str):
        self._client = redis.from_url(redis_url, decode_responses=True)

    async def store(self, fun_fact: DailyFunFact) -> None:
        score = fun_fact.date.toordinal() 
        await self._client.zadd(self.KEY, {fun_fact.fact: score})

    async def get(self, query_date: date) -> Optional[DailyFunFact]:
        score = query_date.toordinal()
        results = await self._client.zrangebyscore(self.KEY, score, score)
        if not results:
            return None

        return DailyFunFact(date=query_date, fact=results[0])
    
    async def get_last_n(self, n: int) -> list[DailyFunFact]:
        results = await self._client.zrevrange(self.KEY, 0, n - 1, withscores=True)
        return [DailyFunFact.from_ordinal(int(score), fact) for fact, score in results]

    async def acquire_lock(self, date: date, ttl: int = 10) -> bool:
        lock_key = self._build_lock_key(date)
        return await self._client.set(lock_key, "1", ex=ttl, nx=True) or False

    async def release_lock(self, date: date):
        lock_key = self._build_lock_key(date)
        await self._client.delete(lock_key)

    def _build_lock_key(self, date: date) -> str:
        return f"{self._LOCK_KEY_PREFIX}{date.isoformat()}"
