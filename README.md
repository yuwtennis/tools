# tools
Group of tools which makes my life easy

* [Environments](#environments)
  * [Docker compose](#docker-compose)
* [Applications](#applications)
  * [Household expenses](#household-expenses)
  * [Economy](#economy)

## Environments
### Docker compose

Directory: `docker/`

Docker compose. Used in my lab environment.

## Applications
### Household expenses

Directory `household_expenses/`

This is migrated into [household-expense](https://github.com/yuwtennis/household-expense)

### Economy

Directory `economy/`

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

### Ping parser

Directory `scripts/ping_parser/`

Parses ping result and send to elasticsearch. Used [ingest pipeline](https://www.elastic.co/guide/en/elasticsearch/reference/7.17/ingest.html) to parse fields.  
I am using this to check network performance when I am outside.

I have tested with elasticsearch `7.17.4` .

#### Getting started

```markdown
# Create ingest pipeline
curl -XPUT _ingest/pipeline/ping-result-parser

# Run script
bash ping.sh
```