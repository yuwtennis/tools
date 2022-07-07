#!/bin/sh

TO="www.google.com"
WIRED_INTERFACE=enp38s0f1
WIRELESS_INTERFACE=wlp0s20f3

function check_interface_state() {
  local INTERFACE=$1

  echo `ip l show $INTERFACE | grep state | cut -d ' ' -f 9`
}

function check_address() {
  local INTERFACE=$1

  echo `ip a show $INTERFACE | grep -w inet | cut -d ' ' -f 6 | cut -d '/' -f 1`
}

function exec_ping() {
  RESULT=`ping -c 3 ${TO} | grep rtt ; echo "$TO $RESULT"`

  echo $RESULT
}

function main() {

  local TIMESTAMP=`date -u --iso-8601=seconds`
  local PING_RESULT=`exec_ping`

  # Decide running interface
  if [ `check_interface_state $WIRED_INTERFACE` == 'UP' ]; then
    RUNNING_INTERFACE=$WIRED_INTERFACE
  elif [  `check_interface_state $WIRELESS_INTERFACE` == 'UP' ]; then
    RUNNING_INTERFACE=$WIRELESS_INTERFACE
  else
    echo 'Expected interface not found'
    exit
  fi

  FROM=`check_address $RUNNING_INTERFACE`

  curl -H 'Content-Type: application/json' \
       -XPOST localhost:9200/ping-result/_doc?pipeline=ping-result-parser -d '
{
  "message": "'"${TIMESTAMP} ${FROM} ${TO} ${PING_RESULT}"'"
}'
}

main
