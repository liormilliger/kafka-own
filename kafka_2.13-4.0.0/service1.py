#!/usr/bin/env python

from random import choice
from confluent_kafka import Producer, Consumer
import time
import json

def create_producer():
    config = {
        'bootstrap.servers': 'localhost:9092',
        'acks': 'all'
    }
    return Producer(config)

def create_consumer():
    consumer_config = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'service1-group',
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(consumer_config)
    consumer.subscribe(['service2'])  # Subscribe to the service2 topic
    return consumer

def delivery_callback(err, msg):
    if err:
        print('ERROR: Message failed delivery: {}'.format(err))
    else:
        print("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
            topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))

def produce_message(producer):
    user_ids = ['user1', 'user2', 'user3']
    products = ['itemA', 'itemB', 'itemC']

    user_id = choice(user_ids)
    product = choice(products)
    message = {'user_id': user_id, 'product': product}

    producer.produce("service1", key=user_id, value=json.dumps(message).encode('utf-8'), callback=delivery_callback)
    producer.poll(1)  # Invoke delivery callback
    print(f"Produced to service1: {message}")

def consume_message(consumer):
    msg = consumer.poll(1.0)
    if msg is None:
        print("Waiting for messages from service2...")
    elif msg.error():
        print("ERROR: {}".format(msg.error()))
    else:
        consumed_message = json.loads(msg.value().decode('utf-8'))
        print("Consumed from service2: key = {key:12} value = {value:12}".format(
            key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))

if __name__ == "__main__":
    producer = create_producer()
    consumer = create_consumer()

    while True:
        produce_message(producer)  # Produce a message to service1 topic
        consume_message(consumer)    # Consume messages from service2 topic
        time.sleep(60)              # Wait for 1 minute before producing the next message
