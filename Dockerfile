FROM python:3.11

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install --no-cache --no-interaction --no-root

COPY /data /app/data
COPY /data_transformer /app/data_transformer

CMD ["uvicorn", "data_transformer.main:app", "--host", "0.0.0.0", "--port", "8000"]