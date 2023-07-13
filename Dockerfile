FROM python:3.9.6-slim as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.5.1

RUN pip install "poetry==$POETRY_VERSION"

FROM builder as production

# Create a non-root user
RUN useradd -m griptape
USER griptape

COPY . .
RUN poetry install --no-dev --no-interaction --no-ansi

CMD ["poetry", "run", "python", "app.py"]
