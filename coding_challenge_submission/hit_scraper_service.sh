#!/bin/sh  

ss_port=$1
prom_port=$2
url=$3

if [ $# -lt 3 ]; then
  echo 1>&2 "$0: not enough arguments - please run with scraper service port, prometheus service port, and url to hit"
  exit 2
elif [ $# -gt 3 ]; then
  echo 1>&2 "$0: too many arguments"
  exit 2
fi

while true  
do  
  echo "Hitting scraper service on port $ss_port, passing url $url"
  echo "{'url': '$url'}"
  curl --header "Content-Type: application/json" --request POST --data "{\"url\": \"$url\"}" 0.0.0.0:$ss_port
  echo "Getting Prometheus metrics"
  curl 0.0.0.0:$2/metrics
  sleep 30  
done