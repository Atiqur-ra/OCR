from confluent_kafka import Producer
import json
from kafka.config import KAFKA_BOOTSTRAP_SERVERS, DOCUMENT_TOPIC
import logging
from logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

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
        logging.error(f"Producer error: {e}")
