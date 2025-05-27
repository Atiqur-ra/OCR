import signal
import sys
import logging
from kafka.consumer import consume_events  # your consumer function
from logging_config import setup_logging

setup_logging()
logger = logging.getLogger("run_consumer")

def main():
    logger.info("Starting Kafka consumer...")
    try:
        consume_events()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

def shutdown(signum, frame):
    logger.info(f"Received signal {signum}. Shutting down...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown)   # Ctrl+C
    signal.signal(signal.SIGTERM, shutdown)  # Termination signal
    main()
