"""stdio entry point (for AI assistants like Claude Desktop / Cursor)."""

from __future__ import annotations

from .appConfig import settings
from .createServer import create_server
from .utils import configure_logging, get_logger

configure_logging()
logger = get_logger("neshan_mcp")


def main() -> None:
    if not settings.has_default_key:
        logger.warning(
            "stdio mode with no NESHAN_API_KEY set. Tools will return an auth "
            "error until a key is provided (set NESHAN_API_KEY in env)."
        )
    logger.info("Starting Neshan MCP (stdio)")
    create_server().run()


if __name__ == "__main__":
    main()
