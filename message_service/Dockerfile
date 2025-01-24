FROM python:3.12-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt update -y && \
    apt install -y python3-dev \
    gcc \
    musl-dev

RUN pip3 install poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry install --only main

COPY . /app/

ENV PYTHONPATH=/app/src

# CMD ["poetry", "run", "python3", "src/message_service/presentation/main.py"]

