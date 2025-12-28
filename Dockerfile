FROM python:3.13-slim

WORKDIR /app

RUN pip install poetry==2.1.1

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && poetry install --no-root --only main

COPY . .

