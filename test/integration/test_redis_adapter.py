import pytest
from datetime import date, timedelta
from unittest.mock import patch

from app.adapter.redis.daily_fun_fact_redis_adapter import FunFactRedisAdapter
from app.domain.model import DailyFunFact


@pytest.mark.integration
class TestFunFactRedisAdapter:

    @pytest.fixture
    def redis_adapter(self, fake_redis):
        adapter = FunFactRedisAdapter("redis://localhost:6379")
        adapter._client = fake_redis
        return adapter

    @pytest.mark.asyncio
    async def test_store_and_get_fun_fact(self, redis_adapter, sample_fun_fact):
        # Act
        await redis_adapter.store(sample_fun_fact)
        result = await redis_adapter.get(sample_fun_fact.date)

        # Assert
        assert result == sample_fun_fact

    @pytest.mark.asyncio
    async def test_get_non_existent_fun_fact(self, redis_adapter):
        # Act
        result = await redis_adapter.get(date(2024, 1, 1))

        # Assert
        assert result is None

    @pytest.mark.asyncio
    async def test_store_multiple_fun_facts(self, redis_adapter, sample_fun_facts):
        # Setup
        for fact in sample_fun_facts:
            await redis_adapter.store(fact)

        # Assert
        for fact in sample_fun_facts:
            result = await redis_adapter.get(fact.date)
            assert result == fact

    @pytest.mark.asyncio
    async def test_get_last_n_fun_facts(self, redis_adapter, sample_fun_facts):
        # Setup
        for fact in sample_fun_facts:
            await redis_adapter.store(fact)

        # Act
        result = await redis_adapter.get_last_n(3)

        # Assert
        assert len(result) == 3
        assert result[0].date == sample_fun_facts[0].date
        assert result[1].date == sample_fun_facts[1].date
        assert result[2].date == sample_fun_facts[2].date

    @pytest.mark.asyncio
    async def test_get_last_n_with_insufficient_facts(self, redis_adapter, sample_fun_facts):
        # Setup
        for fact in sample_fun_facts[:2]:
            await redis_adapter.store(fact)

        # Act
        result = await redis_adapter.get_last_n(5)

        # Assert
        assert len(result) == 2
        assert result[0].date == sample_fun_facts[0].date
        assert result[1].date == sample_fun_facts[1].date

    @pytest.mark.asyncio
    async def test_get_last_n_with_no_facts(self, redis_adapter):
        # Act
        result = await redis_adapter.get_last_n(5)

        # Assert
        assert result == []

    @pytest.mark.asyncio
    async def test_lock_acquire_and_release(self, redis_adapter):
        test_date = date(2024, 1, 15)

        # Act
        acquired1 = await redis_adapter.acquire_lock(test_date)
        acquired2 = await redis_adapter.acquire_lock(test_date)
        await redis_adapter.release_lock(test_date)
        acquired3 = await redis_adapter.acquire_lock(test_date) 

        # Assert
        assert acquired1 is True
        assert acquired2 is False
        assert acquired3 is True

    @pytest.mark.asyncio
    async def test_lock_expiration(self, redis_adapter):
        test_date = date(2024, 1, 15)

        # Act
        acquired1 = await redis_adapter.acquire_lock(test_date, ttl=1)  
        acquired2 = await redis_adapter.acquire_lock(test_date)

        import asyncio
        await asyncio.sleep(1.1)

        acquired3 = await redis_adapter.acquire_lock(test_date) 

        # Assert
        assert acquired1 is True
        assert acquired2 is False
        assert acquired3 is True
