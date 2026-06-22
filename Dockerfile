FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --no-cache-dir -e .

ENV NESHAN_TRANSPORT=http \
    NESHAN_HOST=0.0.0.0 \
    NESHAN_PORT=3000

EXPOSE 3000

CMD ["neshan-mcp-http"]
