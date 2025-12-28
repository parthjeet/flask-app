FROM ghcr.io/astral-sh/uv:python3.12-bookworm AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project

COPY src/ ./

RUN uv sync --frozen --no-dev

FROM python:3.12-slim-bookworm

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app /app

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]