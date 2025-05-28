import json
import os
import threading
import socket
import aiokafka

from custom_types.custom_dict import KafkaProducerMessage
from common.utils import get_logger
logger = get_logger(__name__)


class KafkaProducer:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        conf = {
            'bootstrap_servers': os.getenv("KAFKA_BROKERS"),
            'client_id': socket.gethostname(),
            'enable_idempotence': True,
            'request_timeout_ms': 3000,
            'retry_backoff_ms': 500,
        }
        self.producer = aiokafka.AIOKafkaProducer(**conf)
        logger.info("Successfully initialized kafka brokers")

    async def start_producer(self):
        logger.info("Attempting to start kafka producer")
        await self.producer.start()
        logger.info("Successfully started kafka producer")

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def stop_producer(self):
        self.producer.stop()

    async def send_message(self, topic_name: str, attributes: KafkaProducerMessage):
        try:
            message = json.dumps(attributes.get("value")).encode("utf-8")
            key = attributes.get("key").encode("utf-8")
            logger.info(f"Attempting to send message to kafka ::: {message}")
            await self.producer.send_and_wait(topic=topic_name, value=message, key=key)
            logger.info("Successfully sent message to kafka")
        except Exception as e:
            logger.error("Error occurred while sending message to kafka :::  "+ str(e))