"""Runtime configuration (settings + env-based key lookup)."""

from __future__ import annotations

import os
from dataclasses import dataclass, field

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass

from .constants import BASE_URL, KEY_OVERRIDE_ENV

_DEFAULT_KEY = os.getenv("NESHAN_API_KEY", "")


def env_key_for(service: str) -> str:
    """Env-based key for a service (override env -> default). Fallback for stdio."""
    env_name = KEY_OVERRIDE_ENV.get(service)
    if env_name:
        override = os.getenv(env_name)
        if override:
            return override
    return _DEFAULT_KEY


@dataclass
class Settings:
    base_url: str = BASE_URL
    transport: str = field(default_factory=lambda: os.getenv("NESHAN_TRANSPORT", "stdio"))
    host: str = field(default_factory=lambda: os.getenv("NESHAN_HOST", "127.0.0.1"))
    port: int = field(default_factory=lambda: int(os.getenv("NESHAN_PORT", "3000")))
    timeout: float = field(default_factory=lambda: float(os.getenv("NESHAN_TIMEOUT", "15")))
    max_retries: int = field(default_factory=lambda: int(os.getenv("NESHAN_MAX_RETRIES", "2")))
    log_level: str = field(default_factory=lambda: os.getenv("NESHAN_LOG_LEVEL", "INFO"))

    @property
    def has_default_key(self) -> bool:
        return bool(_DEFAULT_KEY)


settings = Settings()
