FROM python:3.13
LABEL authors="dan"


RUN mkdir /app
WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt  /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/src
COPY .env /app/.env

COPY gunicorn_config.py /app/

