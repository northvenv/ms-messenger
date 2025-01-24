FROM python:3.12.3-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt update -y && \
    apt install -y python3-dev \
    gcc \
    musl-dev

RUN pip3 install poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-root
COPY . /app/

ENV PYTHONPATH=/app/src
