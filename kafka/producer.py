from confluent_kafka import Producer
import json
from kafka.config import KAFKA_BOOTSTRAP_SERVERS, DOCUMENT_TOPIC

producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})

def publish_document_event(data: dict):
    """Publishes document metadata to Kafka."""
    try:
        producer.produce(
            DOCUMENT_TOPIC,
            key=str(data.get('filename')),
            value=json.dumps(data),
            callback=lambda err, msg: print(f'Produced: {msg.value()}' if not err else f'Error: {err}')
        )
        producer.flush()
    except Exception as e:
        print(f"Producer error: {e}")
