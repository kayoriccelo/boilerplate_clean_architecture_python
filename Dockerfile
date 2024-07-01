FROM python:3.8-slim-bullseye

RUN apt-get update

RUN pip install --no-cache-dir --upgrade pip

WORKDIR /code

COPY . .

RUN pip install -r requirements.txt
