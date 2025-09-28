from app.adapter.mistral import get_mistral_adapter
from app.adapter.redis import get_daily_fun_fact_redis_adapter
from app.domain.service.daily_fun_fact_service import DailyFunFactService


_cache_port = get_daily_fun_fact_redis_adapter()
_llm_port = get_mistral_adapter()
_daily_fun_fact_service_instance = DailyFunFactService(_cache_port, _llm_port)

def get_daily_fun_fact_service() -> DailyFunFactService:
    return _daily_fun_fact_service_instance
