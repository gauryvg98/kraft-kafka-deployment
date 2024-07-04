from confluent_kafka.admin import AdminClient
import config

def get_broker_count(bootstrap_servers, admin_client):
    cluster_metadata = admin_client.list_topics(timeout=10)
    brokers = cluster_metadata.brokers
    return len(brokers)

def get_topic_count(bootstrap_servers, admin_client):
    topics = admin_client.list_topics(timeout=10).topics
    return len(topics)

if __name__ == "__main__":
    bootstrap_servers = config.EXTERNAL_IP
    sasl_username = config.SASL_USERNAME
    sasl_password = config.SASL_PASSWORD

    admin_client = AdminClient({
        'bootstrap.servers': bootstrap_servers,
        'security.protocol': 'SASL_PLAINTEXT',
        'sasl.mechanisms': 'PLAIN',
        'sasl.username': sasl_username,
        'sasl.password': sasl_password
    })

    broker_count = get_broker_count(bootstrap_servers, admin_client)
    topic_count = get_topic_count(bootstrap_servers, admin_client)
    
    print(f"Number of brokers in the cluster: {broker_count}")
    print(f"Number of topics in the cluster: {topic_count}")
