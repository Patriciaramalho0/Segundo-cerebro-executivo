from openai import OpenAI
from settings import get_setting

class AIBrain:
    def __init__(self):
        api_key = get_setting("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY não está configurada nos Secrets.")
        self.client = OpenAI(api_key=api_key)
        self.model = get_setting("OPENAI_MODEL", "gpt-4o-mini")

    def ask(self, prompt, system_prompt="Você é um assistente útil."):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=int(get_setting("AI_MAX_OUTPUT_TOKENS", "700"))
        )
        usage = response.usage
        return {
            "content": response.choices[0].message.content or "",
            "model": response.model,
            "prompt_tokens": usage.prompt_tokens if usage else 0,
            "completion_tokens": usage.completion_tokens if usage else 0,
            "total_tokens": usage.total_tokens if usage else 0
        }
