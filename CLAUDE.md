# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This is **neshan-mcp** (v0.3.0): an MCP server wrapping the [Neshan Maps Platform](https://platform.neshan.org/docs) REST API. It exposes search, geocoding, routing, isochrone, distance matrix, TSP, static maps, traffic analytics, zipcode lookup, and VRP as MCP tools usable by Claude Desktop, Cursor, and similar AI clients.

## Commands

```bash
# Install (editable)
pip install -e .

# Run stdio mode (default)
neshan-mcp

# Run HTTP mode
neshan-mcp-http

# Docker
docker build -t neshan-mcp .
docker run -p 3000:3000 --env-file .env neshan-mcp
```

There is no test suite currently. Linting/type checking commands are not configured.

## Architecture

The codebase follows a strict four-layer pipeline: `tool → handler → service → http`

```
tools/         thin MCP interface; only calls handler, never service directly
handlers/      Pydantic validation → service call → normalize errors via @handle_api_errors
services/      map args to Neshan API endpoints; no MCP knowledge
services/base/ NeshanClient — sole network point (httpx, retry, key injection)
```

All domains (`search`, `routing`, `map`, `traffic`, `zipcode`, `vrp`) are organized in parallel across all four layers. `tools/__init__.py:register_all` is the single registration point.

### Key files

- `createServer.py` — FastMCP factory; wires `NeshanClient` lifespan + `register_all`
- `constants.py` — all endpoint paths with `[verified]` / `[VERIFY]` markers; bump versions here
- `appConfig.py` — `Settings` dataclass reads env vars; `env_key_for(service)` for stdio fallback
- `auth/apiKeyResolver.py` — key resolution: HTTP header → per-service header → env fallback
- `utils/apiErrorHandler.py` — `NeshanError`, `handle_api_errors` decorator, error hint map
- `handlers/shared/responseTrimmer.py` — shared response post-processing

### API key resolution

In **HTTP mode**, the client passes the key per-request:
- `Neshan-Api-Key` — used for all services
- `Neshan-Api-Key-<service>` — per-service override (service names: `search`, `geocoding`, `routing`, `historical`, `matrix`, `tsp`, `static`, `static_arc`, `isochrone`, `map_matching`, `traffic`, `zipcode`, `vrp`)
- `Api-Key` — alias

In **stdio mode**, keys fall back to env: `NESHAN_API_KEY` (default) or `NESHAN_KEY_<SERVICE>` per-service overrides (see `constants.py:KEY_OVERRIDE_ENV`).

Static map endpoints send the key as a query param (`key=`) instead of a header — handled in `NeshanClient.get_bytes_with_query_key`.

## Naming convention

File names are **camelCase** (e.g., `searchHandler.py`, `neshanClient.py`) — intentional deviation from Python's `snake_case` convention to stay consistent with the reference layout.

## Adding a new service within an existing domain

Add the method to `<domain>Service`, `<domain>Schema`, `<domain>Handler`, and `<domain>Tools`.

## Adding a new domain

Create a subdirectory in each of `tools/`, `handlers/`, `schemas/`, and `services/`. Register the new tools file in `tools/__init__.py:register_all`.

## Known caveats

- `neshan_reverse_geocode` uses `/v5/reverse`; some accounts require `/v4/reverse` — change `Endpoints.REVERSE` in `constants.py`.
- `neshan_map_matching` endpoint path is **unverified** against live docs; override via `NESHAN_MAP_MATCHING_PATH` env var.
