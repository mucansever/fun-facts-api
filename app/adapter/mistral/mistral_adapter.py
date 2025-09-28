from mistralai import Mistral

from app.domain.port import LlmPort


class MistralAdapter(LlmPort):
    _DEFAULT_MODEL = "mistral-tiny"
    _DEFAULT_TEMP = 1.0
    _MAX_TOKENS = 4096

    def __init__(self, api_key: str):
        self.client = Mistral(api_key=api_key)

    async def chat(
        self,
        prompt: str,
        model: str = _DEFAULT_MODEL,
        temperature: float = _DEFAULT_TEMP,
    ) -> str:
        response = await self.client.chat.complete_async(
            model=model,
            messages=[{"role": "user", "content": prompt}], # type: ignore
            temperature=temperature,
            max_tokens=self._MAX_TOKENS,
        )
        return str(response.choices[0].message.content)
