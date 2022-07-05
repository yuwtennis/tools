#!/bin/sh

TO="www.google.com"
DATE=`date -u --iso-8601=seconds`
PING_RESULT=`ping -c 3 ${TO} | grep rtt` ; echo "$TO $RESULT"

function check_interface_state() {
  local INTERFACE=$1

  echo `ip l show $INTERFACE | grep state | cut -d ' ' -f 9`
}

function check_address() {
  local INTERFACE=$1

  echo `ip a show $INTERFACE | grep -w inet | cut -d ' ' -f 6 | cut -d '/' -f 1`
}

function main() {

  if [ `check_interface_state 'enp38s0f1'` == 'UP' ]; then
    RUNNING_INTERFACE=enp38s0f1
  elif [  `check_interface_state 'wlp0s20f3'` == 'UP' ]; then
    RUNNING_INTERFACE=wlp0s20f3
  else
    echo 'Expected interface not found'
    exit
  fi

  FROM=`check_address $RUNNING_INTERFACE`

  curl -H 'Content-Type: application/json' \
       -XPOST localhost:9200/ping-result/_doc?pipeline=ping-result-parser -d '
{
  "message": "'"${DATE} ${FROM} ${TO} ${PING_RESULT}"'"
}'
}

main
