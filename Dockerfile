FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-cache

COPY . .

EXPOSE 8000
CMD ["uv", "run", "gunicorn", "planetapplication.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
