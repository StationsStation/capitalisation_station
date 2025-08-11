# ---- Builder ----
FROM python:3.11 AS builder

# Install Poetry 1.8.3
RUN pip install --no-cache-dir poetry==1.8.3

# Configure Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Copy lockfile and project metadata
COPY pyproject.toml poetry.lock ./
RUN touch README.md  # If needed for dependencies

# Copy local dependencies (e.g. custom packages)
COPY third_party /app/third_party
RUN ls -la third_party

# Install only main dependencies, skip dev and avoid installing the project itself
RUN --mount=type=cache,target=/tmp/poetry_cache \
    poetry install --only main --no-root

# ---- Runtime ----
FROM python:3.11-slim AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy your application packages
COPY packages /app/packages

WORKDIR /app
RUN autonomy packages sync

CMD ["adev",  "run",  "dev",  "--no-use-tendermint", "--force", "eightballer/derive_arbitrage_agent"]
