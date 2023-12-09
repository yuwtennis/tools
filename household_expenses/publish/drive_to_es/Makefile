
test:
	pytest -s tests/

lint:
	pylint  --extension-pkg-whitelist=pydantic drive_to_es/

static-type-check:
	mypy drive_to_es

build:
	sudo docker build -t drive-to-es:latest .
