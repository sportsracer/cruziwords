# syntax=docker/dockerfile:1
FROM python:3.10-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install .

CMD cruziwords_webserver