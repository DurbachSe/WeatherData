#!/bin/bash

# Start Zookeeper
zookeeper_path=/usr/local/
$zookeeper_path/bin/zookeeper-server-start $zookeeper_path/etc/zookeeper/zoo.cfg &

# Start Kafka
kafka_path=/usr/local/
$kafka_path/bin/kafka-server-start $kafka_path/etc/kafka/server.properties &

# Wait for services to start
sleep 5

# Create Kafka Topic
kafka_topic=weather-data
$kafka_path/bin/kafka-topics.sh --create --topic $kafka_topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
