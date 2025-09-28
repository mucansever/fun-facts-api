import pytest
from datetime import date
from unittest.mock import AsyncMock

from fakeredis import FakeAsyncRedis

from app.domain.model import DailyFunFact
from app.domain.port import LlmPort, DailyFunFactCachePort


@pytest.fixture
def fake_redis() -> FakeAsyncRedis:
    return FakeAsyncRedis(decode_responses=True)


@pytest.fixture
def sample_fun_fact() -> DailyFunFact:
    return DailyFunFact(
        date=date(2024, 1, 15),
        fact="The human brain contains approximately 86 billion neurons."
    )


@pytest.fixture
def sample_fun_facts() -> list[DailyFunFact]:
    return [
        DailyFunFact(date=date(2024, 1, 15), fact="The human brain contains approximately 86 billion neurons."),
        DailyFunFact(date=date(2024, 1, 14), fact="A group of flamingos is called a 'flamboyance'."),
        DailyFunFact(date=date(2024, 1, 13), fact="Honey never spoils - archaeologists have found edible honey in ancient Egyptian tombs."),
        DailyFunFact(date=date(2024, 1, 12), fact="Octopuses have three hearts and blue blood."),
        DailyFunFact(date=date(2024, 1, 11), fact="A single cloud can weigh more than a million pounds."),
    ]


@pytest.fixture
def mock_llm_port() -> AsyncMock:
    mock = AsyncMock(spec=LlmPort)
    mock.chat.return_value = "This is a test fun fact from the mock LLM."
    return mock


@pytest.fixture
def mock_cache_port() -> AsyncMock:
    mock = AsyncMock(spec=DailyFunFactCachePort)
    mock.get.return_value = None
    mock.get_last_n.return_value = []
    mock.acquire_lock.return_value = True
    mock.store.return_value = None
    mock.release_lock.return_value = None
    return mock


@pytest.fixture
def mock_cache_port_with_data(sample_fun_facts) -> AsyncMock:
    mock = AsyncMock(spec=DailyFunFactCachePort)
    mock.get.return_value = sample_fun_facts[0]
    mock.get_last_n.return_value = sample_fun_facts
    mock.acquire_lock.return_value = True
    mock.store.return_value = None
    mock.release_lock.return_value = None
    return mock
