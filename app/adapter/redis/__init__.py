import os

from app.adapter.redis.daily_fun_fact_redis_adapter import FunFactRedisAdapter
from app.domain.port.daily_fun_fact_cache_port import DailyFunFactCachePort


_redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")
_daily_fun_fact_redis_adapter_instance: DailyFunFactCachePort = FunFactRedisAdapter(_redis_url)

def get_daily_fun_fact_redis_adapter() -> DailyFunFactCachePort:
    return _daily_fun_fact_redis_adapter_instance
