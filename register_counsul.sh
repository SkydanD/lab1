#!/usr/bin/env sh


SERVICE_DATA='{
  "Name": "hazelcast-node-'$NUMBER_SERV'",
  "Address": "hazelcast-node-'$NUMBER_SERV'",
  "Port": 5701
}'
echo "$SERVICE_DATA"
curl -X PUT -d "$SERVICE_DATA" http://consul-service:8500/v1/agent/service/register
hz start