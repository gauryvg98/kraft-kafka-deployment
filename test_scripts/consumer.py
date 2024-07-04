from confluent_kafka import Consumer, KafkaException, KafkaError
import config

def create_consumer(bootstrap_servers, group_id, topic):
    # Configure the consumer
    conf = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest',
        'security.protocol': 'SASL_PLAINTEXT',
        'sasl.mechanisms': 'PLAIN',
        'sasl.username': config.SASL_USERNAME,
        'sasl.password': config.SASL_PASSWORD
    }

    # Create a Consumer instance
    consumer = Consumer(conf)

    # Subscribe to the topic
    consumer.subscribe([topic])

    return consumer

def consume_messages(consumer):
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    print(f'%% {msg.topic()} [{msg.partition()}] reached end at offset {msg.offset()}')
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                print(f'Received message: {msg.value().decode("utf-8")}')
    except KeyboardInterrupt:
        pass
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

if __name__ == "__main__":
    bootstrap_servers = config.EXTERNAL_IP  # Replace with your Kafka bootstrap server
    group_id = 'my-group'  # Replace with your consumer group ID
    topic = 'test-topic'  # Replace with your topic name

    consumer = create_consumer(bootstrap_servers, group_id, topic)
    consume_messages(consumer)