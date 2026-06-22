"""HTTP entry point. Clients send the key per request in the 'Neshan-Api-Key' header."""

from __future__ import annotations

from .appConfig import settings
from .createServer import create_server
from .utils import configure_logging, get_logger

configure_logging()
logger = get_logger("neshan_mcp")


def main() -> None:
    if not settings.has_default_key:
        logger.info(
            "No NESHAN_API_KEY set; expecting clients to send the key in the "
            "'Neshan-Api-Key' header per request."
        )
    logger.info("Starting Neshan MCP (HTTP) on %s:%s", settings.host, settings.port)
    create_server().run(transport="http", host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
