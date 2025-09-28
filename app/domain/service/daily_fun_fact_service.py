from datetime import date
from typing import Optional

from app.util import logger

from app.domain.port import LlmPort, DailyFunFactCachePort
from app.domain.model import DailyFunFact


class DailyFunFactService:

    _BASE_PROMPT = "Tell me a random fun fact. Your response MUST be only the fun fact. It must be different from these: "

    def __init__(self, cache_port: DailyFunFactCachePort, llm_port: LlmPort):
        self.cache_port = cache_port
        self.llm_port = llm_port
        self.cached_prompt_date = None
        self.cached_prompt = ""

    async def get_todays_fun_fact(self) -> Optional[DailyFunFact]:
        today = date.today()
        fact = await self.cache_port.get(today)
        if fact:
            return fact

        fact = None
        lock_acquired = await self.cache_port.acquire_lock(today)

        try:
            if lock_acquired:
                fact = await self.cache_port.get(today)
                if not fact:
                    prompt = await self._get_prompt(today)
                    fact_text = await self.llm_port.chat(prompt)
                    fact = DailyFunFact(today, fact_text)
                    await self.cache_port.store(fact)
        finally:
            if lock_acquired:
                await self.cache_port.release_lock(today)

        return fact
    
    async def get_last_n_fun_facts(self, n: int) -> list[DailyFunFact]:
        return await self.cache_port.get_last_n(n)
    
    async def _get_prompt(self, date: date) -> str:
        if date == self.cached_prompt_date:
            return self.cached_prompt

        recent_fun_facts = await self.get_last_n_fun_facts(10) # increase randomness
        recent_fun_facts_str = ",".join([f'`{fun_fact.fact}`' for fun_fact in recent_fun_facts])

        self.cached_prompt = f"{self._BASE_PROMPT} + [{recent_fun_facts_str}]"
        self.cached_prompt_date = date

        logger.info(self.cached_prompt)

        return self.cached_prompt
