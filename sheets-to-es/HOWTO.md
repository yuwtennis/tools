
# Init
1. Init GAS
```
make -f Makefile.gas init SHEET=MY_SHEET_ID
```

# Run

```
export SERVICE_ACCOUNT_DATA=`cat MY_SERVICE_ACCOUNT_FILE`
````

# Deploy

1. Deploy to GAS
```
make -f Makefile.gas push
```

2. Deploy app to Kubernetes
TBC
