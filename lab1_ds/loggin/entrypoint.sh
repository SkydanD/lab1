#!/usr/bin/env sh

SERVICE_DATA='{
  "Name": "'$SERVICE_NAME'",
  "Address": "'$SERVICE_NAME'",
  "Port": '$PORT_SEVICE'
}'

curl -X PUT -d "$SERVICE_DATA" http://consul-service:8500/v1/agent/service/register

python main.py