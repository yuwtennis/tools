ES_HOST := http://elasticsearch:9200
SERVICE_ACCOUNT_FILE := /app/elite-caster-125113-90bc4da32331.json

build:
	sudo docker build --build-arg SERVICE_ACCOUNT_FILE=$(SERVICE_ACCOUNT_FILE) --build-arg ES_HOST=$(ES_HOST) -t sheets-to-es:latest .
