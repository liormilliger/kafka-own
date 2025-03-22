#!/usr/bin/env python

from confluent_kafka import Consumer, Producer
import json

if __name__ == '__main__':

    # Configuration for Consumer
    consumer_config = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'service2-group',
        'auto.offset.reset': 'earliest'
    }

    # Create Consumer instance
    consumer = Consumer(consumer_config)

    # Subscribe to topic
    topic1 = "service1"
    topic2 = "service2"
    consumer.subscribe([topic1])

    # Configuration for Producer
    producer_config = {
        'bootstrap.servers': 'localhost:9092',
        'acks': 'all'
    }

    # Create Producer instance
    producer = Producer(producer_config)

    # Poll for new messages from Kafka and process them
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                print("Waiting for messages...")
            elif msg.error():
                print("ERROR: {}".format(msg.error()))
            else:
                # Process the received message
                consumed_message = json.loads(msg.value().decode('utf-8'))
                print("Consumed from topic {topic}: key = {key:12} value = {value:12}".format(
                    topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))

                # Produce to the new topic
                producer.produce(topic2, key=msg.key(), value=msg.value(), callback=lambda err, m: print(f"Produced to topic {m.topic()}"))
                producer.poll(1)  # Ensure delivery callback gets called
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
