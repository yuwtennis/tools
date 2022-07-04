
FROM=`ip a show dev wlp0s20f3 | grep -w inet | cut -d ' ' -f 6 | cut -d '/' -f 1`
TO="www.google.com"
DATE=`date -u --iso-8601=seconds`
RESULT=`ping -c 3 ${TO} | grep rtt` ; echo "$TO $RESULT"

curl -H 'Content-Type: application/json' \
     -XPOST localhost:9200/ping-result/_doc?pipeline=ping-result-parser -d '
{
  "message": "'"${DATE} ${FROM} ${TO} ${RESULT}"'"
}
'