import json
import os
import threading
import socket
import aiokafka

from custom_types.custom_dict import KafkaProducerMessage
from common.utils import get_logger
logger = get_logger(__name__)


class KafkaProducer:
    __instance = None
    __lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    cls.__instance = super.__new__(cls)
                    cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        if self.__initialized:
            return
        conf = {
            'bootstrap_servers': os.getenv("KAFKA_BROKERS"),
            'client_id': socket.gethostname(),
            'enable_idempotence': True,
            'request_timeout_ms': 3000,
            'retry_backoff_ms': 500,
        }
        self.producer = aiokafka.AIOKafkaProducer(**conf)
        self.__initialized = True
        logger.info("Successfully initialized kafka brokers")

    async def start_producer(self):
        logger.info("Attempting to start kafka producer")
        await self.producer.start()
        logger.info("Successfully started kafka producer")

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