FROM python:3.9-alpine

WORKDIR /app
ADD ./requirements.txt /app

RUN pip install -r requirements.txt

ARG SERVICE_ACCOUNT_FILE
ARG ES_HOST

ENV SERVICE_ACCOUNT_FILE=$SERVICE_ACCOUNT_FILE
ENV ES_HOST=$ES_HOST

ADD . /app
