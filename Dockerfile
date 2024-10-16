FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY data_transformer /app/data_transformer

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "data_transformer.main:app", "--host", "0.0.0.0", "--port", "8000"]
