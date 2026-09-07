import json

from openai import APIConnectionError, APITimeoutError, OpenAI, RateLimitError

from pydantic import ValidationError

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from ai.configs import settings

from ai.pydantic import Failure_Anaylsis_outputs

deepseek = OpenAI(
    api_key=settings.deepseek_api_key,
    base_url=settings.deepseek_base_url,
    timeout=settings.request_timeout,
    max_retries=0,
)

SYSTEM_PROMPT = "你是一名资深的测试专家。"


@retry(
    retry=retry_if_exception_type((APIConnectionError, APITimeoutError, RateLimitError)),
    stop=stop_after_attempt(settings.max_retries),
    wait=wait_exponential(multiplier=1, min=1, max=10),
)
def _create_chat(prompt: str) -> str:
    response = deepseek.chat.completions.create(
        model=settings.deepseek_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content


def _extract_json(content: str) -> dict:
    text = content.strip()

    if text.startswith("```"):
        text = text.removeprefix("```json").removeprefix("```").rstrip("`").strip()

    return json.loads(text)


def ask_ai(prompt: str) -> Failure_Anaylsis_outputs:
    content = _create_chat(prompt) or ""

    try:
        return Failure_Anaylsis_outputs.model_validate(_extract_json(content))
    except (json.JSONDecodeError, ValidationError):
        return Failure_Anaylsis_outputs(
            classification="unknown",
            confidence=0.0,
            root_cause=f"模型未返回合法 JSON，原始输出：{content[:500]}",
            evidence=[],
            recommendation=["检查 system_prompt 的输出格式约束；连续出现时考虑增加 few-shot 示例"],
        )
