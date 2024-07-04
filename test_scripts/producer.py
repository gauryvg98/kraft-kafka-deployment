from confluent_kafka import Producer
import config 

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def produce_message(bootstrap_servers, topic, message):
    conf = {
        'bootstrap.servers': bootstrap_servers,
        'security.protocol': 'SASL_PLAINTEXT',
        'sasl.mechanisms': 'PLAIN',
        'sasl.username': config.SASL_USERNAME,
        'sasl.password': config.SASL_PASSWORD
    }
    
    p = Producer(conf)

    p.produce(topic, message.encode('utf-8'), callback=delivery_report)

    # Wait for any outstanding messages to be delivered and delivery report
    # callbacks to be triggered.
    p.flush()

if __name__ == "__main__":
    bootstrap_servers = config.EXTERNAL_IP  # Replace with your Kafka bootstrap server
    topic = 'test-topic'  # Replace with your topic name
    message = 'Hello, Kafka!'  # Replace with your message

    produce_message(bootstrap_servers, topic, message)
