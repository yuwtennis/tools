# tools
Group of tools which makes my life easy

* [Environments](#environments)
  * [Docker compose](#docker-compose)
* [Applications](#applications)
  * [Household expenses](#household-expenses)
  * [Stocks](#stocks)

## Environments
### Docker compose
Docker compose. Used in my lab environment.

## Applications
### Household expenses
I manage household expenses in Google Sheets.   
These are apps used by me that makes things comfortable.

Parse data from google sheets and put to drive (_publish/sheet_to_drive_).  
Drive uploaded file can be loaded to elasticsearch. (_publish/drive_to_es_)

Also, in the expense sheet,   
additional sheet can be created by replicating template sheet that is prepared in advance.
(_create_sheet_by_month_)

```
Google Sheets -------> Google Drive ----------> Elasticsearch
              (By GAS)              (By python)
```

### Stocks
Crawls yahoo finance and send to elasticsearch for nice kibana dashboard.

#### Getting started

Available environment variables

| Variable    | Description                                             | Default    |
|-----|---------------------------------------------------------|-----|
| BACKEND_TYPE    | Backends to use. Options are<br>stdout<br>elasticsearch | stdout    |
| ES_HOST    | Elasticsearch host to connect to.                       | localhost    |


```markdown
# Build
make build

# Test
make test
```