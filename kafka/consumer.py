from confluent_kafka import Consumer, KafkaError
import json
import logging
from kafka.config import KAFKA_BOOTSTRAP_SERVERS, DOCUMENT_TOPIC, GROUP_ID
from services.document_processor import process_document_task
from logging_config import setup_logging


setup_logging()
logger = logging.getLogger(__name__)

consumer_conf = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'group.id': GROUP_ID,
    'auto.offset.reset': 'earliest'
}

def consume_events():
    """
    Start consuming document upload events from the Kafka topic and process each message.
    This function will run indefinitely unless interrupted.
    """
    consumer = Consumer(consumer_conf)
    consumer.subscribe([DOCUMENT_TOPIC])

    logging.info("Kafka consumer started. Listening on topic: %s", DOCUMENT_TOPIC)

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() != KafkaError._PARTITION_EOF:
                    logging.error("Kafka error: %s", msg.error())
                continue

            try:
                data = json.loads(msg.value().decode('utf-8'))
                logging.info("New message received: %s", data)

                # Basic validation
                if "file_url" not in data or "uploaded_by" not in data:
                    logging.warning("Invalid message format: missing 'file_url' or 'uploaded_by'")
                    continue

                process_document_task(data)

            except json.JSONDecodeError as e:
                logging.error("JSON decode error: %s", e)
            except Exception as e:
                logging.exception("Error while processing message: %s", e)

    except KeyboardInterrupt:
        logging.info("Kafka consumer interrupted. Shutting down gracefully.")
    finally:
        consumer.close()
        logging.info("Kafka consumer closed.")