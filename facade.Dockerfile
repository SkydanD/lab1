# syntax=docker/dockerfile:1

# pull official base image
FROM python:3.11.1-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apk update && apk add gcc python3-dev musl-dev

WORKDIR  /lab1_ds/facade
COPY  /lab1_ds/facade  /lab1_ds/facade/

RUN python -m venv venv
ENV PATH venv/bin:$PATH

RUN pip install --upgrade pip
RUN pip install -r requirments-fast-api.txt

EXPOSE 8015/TCP
ENTRYPOINT ["./entrypoint.sh"]