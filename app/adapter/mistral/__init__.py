import os

from app.adapter.mistral.mistral_adapter import MistralAdapter
from app.domain.port.llm_port import LlmPort


_mistral_api_key = os.getenv("MISTRAL_API_KEY", "")
_mistral_adapter_instance: LlmPort = MistralAdapter(_mistral_api_key)

def get_mistral_adapter() -> LlmPort:
    return _mistral_adapter_instance
