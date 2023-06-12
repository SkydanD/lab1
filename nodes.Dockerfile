# syntax=docker/dockerfile:1

# pull official base image
FROM hazelcast/hazelcast:latest

WORKDIR /opt/hazelcast/
COPY register_counsul.sh /opt/hazelcast/

ENTRYPOINT ["./register_counsul.sh"]