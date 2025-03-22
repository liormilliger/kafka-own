Install kafka on mac:
https://www.freecodecamp.org/news/apache-kafka-handbook/#heading-brokers-in-kafka

Run brew install kafka in a terminal. This will install Kafka's binaries at usr/local/bin.
Finally, run kafka-topics --version in a terminal and you should see 3.3.1. If you do, you're all set.
To make it easier to work with Kafka, you can add Kafka to the PATH environment variable. Open your ~/.bashrc (if using Bash) or ~/.zshrc (if using Zsh) and add the following line, replacing USERNAME with your username:
PATH="$PATH:/Users/USERNAME/kafka_2.13-3.3.1/bin"

Install Java (openjdk-17-jdk)
And export the path or save it in the ~/.zshrc file and source it

Download the kafka-cli:

wget https://archive.apache.org/dist/kafka/3.3.1/kafka_2.13-3.3.1.tgz
And export it in ~/.zshrc
PATH="$PATH:home/USERNAME/kafka_2.13-3.3.1/bin"

Run kafka-topics.sh --version in a terminal and you should see 3.3.1. If you do, you're all set.

Kafka with python:
https://developer.confluent.io/get-started/python/#create-project




Create Project
Create a new directory anywhere you'd like for this project:
mkdir kafka-python-getting-started && cd kafka-python-getting-started
Create and activate a Python virtual environment to give yourself a clean, isolated workspace. You may also use venv if you prefer.

python3 -m venv myenv
source myenv/bin/activate
pip3 install confluent-kafka

virtualenv env

source env/bin/activate
Install the Apache Kafka Python client library:
pip install confluent-kafka
Create Topic
A topic is an immutable, append-only log of events. Usually, a topic is comprised of the same kind of events, e.g., in this guide we create a topic for retail purchases.
Create a new topic, purchases, which you will use to produce and consume events.
Depending on your available Kafka cluster, you have multiple options for creating a topic. You may have access to Confluent Control Center, where you can create a topic with a UI. You may have already installed a Kafka distribution, in which case you can use the kafka-topics command. Note that, if your cluster is centrally managed, you may need to request the creation of a topic from your operations team.
Build Producer
Let's create the Python producer application by pasting the following code into a file producer.py.

#!/usr/bin/env python

from random import choice
from confluent_kafka import Producer

if __name__ == '__main__':

    config = {
        # User-specific properties that you must set
        'bootstrap.servers': 'localhost:9092',

        # Fixed properties
        'acks': 'all'
    }

    # Create Producer instance
    producer = Producer(config)

    # Optional per-message delivery callback (triggered by poll() or flush())
    # when a message has been successfully delivered or permanently
    # failed delivery (after retries).
    def delivery_callback(err, msg):
        if err:
            print('ERROR: Message failed delivery: {}'.format(err))
        else:
            print("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
                topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))

    # Produce data by selecting random values from these lists.
    topic = "purchases"
    user_ids = ['eabara', 'jsmith', 'sgarcia', 'jbernard', 'htanaka', 'awalther']
    products = ['book', 'alarm clock', 't-shirts', 'gift card', 'batteries']

    count = 0
    for _ in range(10):
        user_id = choice(user_ids)
        product = choice(products)
        producer.produce(topic, product, user_id, callback=delivery_callback)
        count += 1

    # Block until the messages are sent.
    producer.poll(10000)
    producer.flush()
Fill in the appropriate bootstrap.servers value and any additional security configuration needed inline where the client configuration config object is created.

Build Consumer
Next, create the Python consumer application by pasting the following code into a file consumer.py.

#!/usr/bin/env python

from confluent_kafka import Consumer

if __name__ == '__main__':

    config = {
        # User-specific properties that you must set
        'bootstrap.servers': 'localhost:9092',

        # Fixed properties
        'group.id':          'kafka-python-getting-started',
        'auto.offset.reset': 'earliest'
    }

    # Create Consumer instance
    consumer = Consumer(config)

    # Subscribe to topic
    topic = "purchases"
    consumer.subscribe([topic])

    # Poll for new messages from Kafka and print them.
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                print("Waiting...")
            elif msg.error():
                print("ERROR: %s".format(msg.error()))
            else:
                # Extract the (optional) key and value, and print.
                print("Consumed event from topic {topic}: key = {key:12} value = {value:12}".format(
                    topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
Again, fill in the appropriate bootstrap.servers value and any additional security configuration needed inline where the client configuration config object is created.


Produce Events
Make the producer script executable, and run it:

chmod u+x producer.py

./producer.py
You should see output resembling this:


Produced event to topic purchases: key = jsmith     value = batteries
Produced event to topic purchases: key = jsmith     value = book
Produced event to topic purchases: key = jbernard   value = book
Produced event to topic purchases: key = eabara     value = alarm clock
Produced event to topic purchases: key = htanaka    value = t-shirts
Produced event to topic purchases: key = jsmith     value = book
Produced event to topic purchases: key = jbernard   value = book
Produced event to topic purchases: key = awalther   value = batteries
Produced event to topic purchases: key = eabara     value = alarm clock
Produced event to topic purchases: key = htanaka    value = batteries

Consume Events
Make the consumer script executable and run it:

chmod u+x consumer.py

./consumer.py
You should see output resembling this:


Consumed event from topic purchases: key = sgarcia    value = t-shirts
Consumed event from topic purchases: key = htanaka    value = alarm clock
Consumed event from topic purchases: key = awalther   value = book
Consumed event from topic purchases: key = sgarcia    value = gift card
Consumed event from topic purchases: key = eabara     value = t-shirts
Consumed event from topic purchases: key = eabara     value = t-shirts
Consumed event from topic purchases: key = jsmith     value = t-shirts
Consumed event from topic purchases: key = htanaka    value = batteries
Consumed event from topic purchases: key = htanaka    value = book
Consumed event from topic purchases: key = sgarcia    value = book
Waiting...
Waiting...
Waiting...
Rerun the producer to see more events, or feel free to modify the code as necessary to create more or different events.
Once you are done with the consumer, enter Ctrl-C to terminate the consumer application.


