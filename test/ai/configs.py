from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    deepseek_api_key: str = ""

    deepseek_base_url: str = "https://api.deepseek.com"

    deepseek_model: str = "deepseek-chat"

    request_timeout: float = 60.0

    max_retries: int = 3

    max_traceback_lines: int = 30

    report_dir: str = "ai_reports"


settings = Settings()

if not settings.deepseek_api_key:
    raise RuntimeError("没有可使用的 API_key，请在项目根目录 .env 中配置 DEEPSEEK_API_KEY")

DeepSeek_api_key = settings.deepseek_api_key
