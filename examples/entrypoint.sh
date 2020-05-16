#!/bin/sh
set -eux

aws sns create-topic --endpoint-url=${GOAWS_URL} --name=loafer__notification
topic=$(aws sns list-topics --endpoint-url=${GOAWS_URL} | grep loafer | cut -d\" -f4)

aws sqs create-queue --endpoint-url=${GOAWS_URL} --queue-name=echo__loafer__notification
queue_url=$(aws sqs list-queues --endpoint-url=${GOAWS_URL} | grep loafer | cut -d\" -f2)

aws sns subscribe --endpoint-url=${GOAWS_URL} --topic-arn ${topic} --protocol sqs --notification-endpoint ${queue_url}

aws sns publish --endpoint-url=${GOAWS_URL} --topic-arn ${topic} --message file://examples/sample.json
exec python -m examples.echo
