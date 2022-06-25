FROM python:3.10-slim-bullseye

WORKDIR /app
ADD ./requirements.txt ./
RUN pip install -r requirements.txt
ADD . ./
