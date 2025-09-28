import pytest
from datetime import date
from unittest.mock import AsyncMock, patch

from app.domain.service.daily_fun_fact_service import DailyFunFactService
from app.domain.model import DailyFunFact


@pytest.mark.unit
class TestDailyFunFactService:

    @pytest.fixture
    def service(self, mock_cache_port, mock_llm_port):
        return DailyFunFactService(mock_cache_port, mock_llm_port)

    @pytest.mark.asyncio
    async def test_get_todays_fun_fact_when_cached(self, service, mock_cache_port, mock_llm_port, sample_fun_fact):
        # Setup
        mock_cache_port.get.return_value = sample_fun_fact

        # Act
        result = await service.get_todays_fun_fact()

        # Assert
        assert result == sample_fun_fact
        mock_cache_port.get.assert_called_once_with(date.today())
        mock_cache_port.acquire_lock.assert_not_called()
        mock_llm_port.chat.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_todays_fun_fact_when_not_cached_and_lock_acquired(self, service, mock_cache_port, mock_llm_port):
        # Setup
        today = date.today()
        mock_cache_port.get.return_value = None
        mock_cache_port.acquire_lock.return_value = True
        mock_llm_port.chat.return_value = "very fun fact"
        expected_fact = DailyFunFact(today, "very fun fact")

        # Act
        result = await service.get_todays_fun_fact()

        # Assert
        assert result == expected_fact
        assert mock_cache_port.get.call_count == 2 
        mock_cache_port.acquire_lock.assert_called_once_with(today)
        mock_llm_port.chat.assert_called_once()
        mock_cache_port.store.assert_called_once_with(expected_fact)
        mock_cache_port.release_lock.assert_called_once_with(today)

    @pytest.mark.asyncio
    async def test_get_todays_fun_fact_when_not_cached_and_lock_not_acquired(self, service, mock_cache_port, mock_llm_port):
        # Setup
        mock_cache_port.get.return_value = None
        mock_cache_port.acquire_lock.return_value = False

        # Act
        result = await service.get_todays_fun_fact()

        # Assert
        assert result is None
        mock_cache_port.get.assert_called_once()
        mock_cache_port.acquire_lock.assert_called_once()
        mock_llm_port.chat.assert_not_called()
        mock_cache_port.store.assert_not_called()
        mock_cache_port.release_lock.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_todays_fun_fact_when_cached_after_lock(self, service, mock_cache_port, mock_llm_port, sample_fun_fact):
        # Setup
        today = date.today()
        mock_cache_port.get.side_effect = [None, sample_fun_fact] 
        mock_cache_port.acquire_lock.return_value = True

        # Act
        result = await service.get_todays_fun_fact()

        # Assert
        assert result == sample_fun_fact
        assert mock_cache_port.get.call_count == 2
        mock_cache_port.acquire_lock.assert_called_once_with(today)
        mock_llm_port.chat.assert_not_called()
        mock_cache_port.store.assert_not_called()
        mock_cache_port.release_lock.assert_called_once_with(today)

    @pytest.mark.asyncio
    async def test_get_last_n_fun_facts(self, service, mock_cache_port, sample_fun_facts):
        # Setup
        n = 3
        mock_cache_port.get_last_n.return_value = sample_fun_facts[:n]

        # Act
        result = await service.get_last_n_fun_facts(n)

        # Assert
        assert result == sample_fun_facts[:n]
        mock_cache_port.get_last_n.assert_called_once_with(n)

    @pytest.mark.asyncio
    async def test_get_prompt_caching(self, service, mock_cache_port, sample_fun_facts):
        # Setup
        test_date = date(2024, 1, 15)
        mock_cache_port.get_last_n.return_value = sample_fun_facts

        # Act
        prompt1 = await service._get_prompt(test_date)
        prompt2 = await service._get_prompt(test_date)

        # Assert
        assert prompt1 == prompt2
        assert mock_cache_port.get_last_n.call_count == 1 

    @pytest.mark.asyncio
    async def test_get_prompt_different_dates(self, service, mock_cache_port, sample_fun_facts):
        # Setup
        date1 = date(2024, 1, 15)
        date2 = date(2024, 1, 16)
        mock_cache_port.get_last_n.return_value = sample_fun_facts

        # Act
        prompt1 = await service._get_prompt(date1)
        prompt2 = await service._get_prompt(date2)

        # Assert
        assert prompt1 == prompt2
        assert mock_cache_port.get_last_n.call_count == 2 

    @pytest.mark.asyncio
    async def test_get_prompt_includes_recent_facts(self, service, mock_cache_port, sample_fun_facts):
        # Setup
        test_date = date(2024, 1, 15)
        mock_cache_port.get_last_n.return_value = sample_fun_facts

        # Act
        prompt = await service._get_prompt(test_date)

        # Assert
        assert service._BASE_PROMPT in prompt
        for fact in sample_fun_facts:
            assert f"`{fact.fact}`" in prompt

    @pytest.mark.asyncio
    async def test_get_prompt_with_empty_recent_facts(self, service, mock_cache_port):
        # Setup
        test_date = date(2024, 1, 15)
        mock_cache_port.get_last_n.return_value = []

        # Act
        prompt = await service._get_prompt(test_date)

        # Assert
        assert service._BASE_PROMPT in prompt
        assert "[]" in prompt 

    @pytest.mark.asyncio
    async def test_lock_release_on_exception(self, service, mock_cache_port, mock_llm_port):
        # Setup
        today = date.today()
        mock_cache_port.get.return_value = None
        mock_cache_port.acquire_lock.return_value = True
        mock_llm_port.chat.side_effect = Exception("LLM error")

        # Assert
        with pytest.raises(Exception, match="LLM error"):
            await service.get_todays_fun_fact()

        mock_cache_port.release_lock.assert_called_once_with(today)

    @pytest.mark.asyncio
    async def test_lock_not_released_when_not_acquired(self, service, mock_cache_port, mock_llm_port):
        # Setup
        mock_cache_port.get.return_value = None
        mock_cache_port.acquire_lock.return_value = False

        # Act
        result = await service.get_todays_fun_fact()

        # Assert
        assert result is None
        mock_cache_port.release_lock.assert_not_called()
