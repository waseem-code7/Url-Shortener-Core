import asyncio
import os
import threading
import socket

from confluent_kafka import Producer
from types.custom_dict import KafkaProducerMessage
from common.utils import get_logger
logger = get_logger(__name__)


class KafkaProducer:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        conf = {
            'bootstrap.servers': os.getenv("KAFKA_BROKERS"),
            'client.id': socket.gethostname()
        }
        self.producer = Producer(conf)
        logger.info("Successfully initialized kafka brokers")

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def poll_producer(self):
        self.producer.poll()


    def send_message(self, topic_name: str, attributes: KafkaProducerMessage, retries=3):

        def acked(err, msg):
            if err is not None:
                logger.info("Failed to deliver message: %s: %s" % (str(msg), str(err)))

                if retries > 0:
                    logger.info("Retrying sending message to kafka ::: ")
                    return self.send_message(topic_name, attributes, retries - 1)
                else:
                    logger.error("All attempts failed to push to kafka hence returning")
            else:
                logger.info("Message produced: %s" % (str(msg)))

        self.producer.produce(topic_name, key=attributes.get("key"), value=attributes.get("value"), callback=acked)
