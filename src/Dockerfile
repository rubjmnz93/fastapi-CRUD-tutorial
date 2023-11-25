FROM python:3.11.0-alpine

WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

ARG DEV=false
RUN set -eux \
    && python -m venv /py \
    && apk add --no-cache --virtual .build-deps build-base \
         openssl-dev libffi-dev gcc musl-dev python3-dev \
    && /py/bin/pip install --upgrade pip setuptools wheel \
    && /py/bin/pip install -r /tmp/requirements.txt \
    && if [ $DEV = "true" ]; \
          then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
      fi \
    && rm -rf /root/.cache/pip \
    && rm -rf /tmp \
    && adduser \
        --disabled-password \
        --no-create-home \
        fastapi-user

COPY . /usr/src/app/

ENV PATH="/py/bin:$PATH"

USER fastapi-user