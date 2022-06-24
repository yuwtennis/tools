# tools
Group of tools which makes my life easy

## household expenses
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

## docker compose
Docker compose. Used in my lab environment.

## Stocks
Crawls yahoo finance and send to elasticsearch for nice kibana dashboard.