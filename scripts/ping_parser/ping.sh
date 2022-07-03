
URL="www.google.com"
DATE=`date -u --iso-8601=seconds`
RESULT=`ping -c 3 ${URL} | grep rtt` ; echo "$URL $RESULT"

curl -H 'Content-Type: application/json' \
     -XPOST localhost:9200/ping-result/_doc?pipeline=ping-result-parser -d '
{
  "message": "'"${DATE} ${URL} ${RESULT}"'"
}
'