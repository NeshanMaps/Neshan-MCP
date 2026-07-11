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


def _getenv(name: str, default: str = "") -> str:
    """os.getenv, stripped of accidental wrapping quotes some deploy templating leaves in."""
    value = os.getenv(name, default)
    return value.strip().strip("\"'") if value else value


def _getenv_list(name: str, default: str) -> list[str]:
    """Comma-separated env var -> list of trimmed, non-empty items."""
    raw = _getenv(name, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


_DEFAULT_KEY = _getenv("NESHAN_API_KEY")


def env_key_for(service: str) -> str:
    """Env-based key for a service (override env -> default). Fallback for stdio."""
    env_name = KEY_OVERRIDE_ENV.get(service)
    if env_name:
        override = _getenv(env_name)
        if override:
            return override
    return _DEFAULT_KEY


@dataclass
class Settings:
    base_url: str = BASE_URL
    transport: str = field(default_factory=lambda: _getenv("NESHAN_TRANSPORT", "stdio"))
    host: str = field(default_factory=lambda: _getenv("NESHAN_HOST", "127.0.0.1"))
    port: int = field(default_factory=lambda: int(_getenv("NESHAN_PORT", "3000")))
    timeout: float = field(default_factory=lambda: float(_getenv("NESHAN_TIMEOUT", "15")))
    max_retries: int = field(default_factory=lambda: int(_getenv("NESHAN_MAX_RETRIES", "2")))
    log_level: str = field(default_factory=lambda: _getenv("NESHAN_LOG_LEVEL", "INFO"))
    # Host/Origin header allow-lists for FastMCP's DNS-rebinding guard. Behind a
    # proxy/NodePort the inbound Host is the external addr, not the bind host, so
    # the guard 421s unless it's listed. Default "*" (trust all) since access is
    # gated by per-request API keys; tighten via NESHAN_ALLOWED_HOSTS if needed.
    allowed_hosts: list[str] = field(
        default_factory=lambda: _getenv_list("NESHAN_ALLOWED_HOSTS", "*")
    )
    allowed_origins: list[str] = field(
        default_factory=lambda: _getenv_list("NESHAN_ALLOWED_ORIGINS", "*")
    )

    @property
    def has_default_key(self) -> bool:
        return bool(_DEFAULT_KEY)


settings = Settings()
