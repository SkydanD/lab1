# syntax=docker/dockerfile:1

# pull official base image
FROM python:3.11.1-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apk update && apk add gcc python3-dev musl-dev curl

WORKDIR /lab1_ds/message
RUN python -m venv venv
ENV PATH venv/bin:$PATH

COPY requerments.txt /lab1_ds/message/
RUN pip install --upgrade pip
RUN pip install -r requerments.txt


COPY  /lab1_ds/global_utils.py  /lab1_ds/message/
COPY /lab1_ds/message /lab1_ds/message/

COPY __init__.py /lab1_ds/message/venv/lib/python3.11/site-packages/hazelcast/__init__.py

ENTRYPOINT ["./entrypoint.sh"]