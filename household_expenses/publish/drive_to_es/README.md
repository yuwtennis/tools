
## Build

```shell
make build 
```

## Run

```shell
docker run \
  -e ES_HOST=YOUR_ES_HOST \
  -e SERVICE_ACCOUNT_INFO=YOUR_SVC_ACCOUNT_INFO \
  drive_to_es:latest python3 __main__.py
```