import os

from fastapi import BackgroundTasks

from services.counter import CounterService
from services.kafka import KafkaProducer
from services.shortener import Shortener
from repository.shortener import ShortenerRepository
from datetime import datetime, timezone, timedelta
from common import utils
from custom_types.custom_dict import KafkaProducerMessage
from dtos.ResponseDTOs import CreateShortUrlResponse, UpdateShortUrlResponse

logger = utils.get_logger("short_url_service.py")


class ShortUrlService:

    def __init__(self, counter_service: CounterService, shortener: Shortener, kafka_producer: KafkaProducer, shortener_repository: ShortenerRepository):
        self.counter_service = counter_service
        self.shortener = shortener
        self.kafka_producer = kafka_producer
        self.shortener_repository = shortener_repository

    def create_new_short_url(self, long_url):
        counter_val = self.counter_service.get_counter_value_safe(retries=2)
        short_url_id = self.shortener.get_short_id(counter_val)

        now = datetime.now(tz=timezone.utc)
        created_at = int(now.timestamp())
        expires_at = int((now + timedelta(hours=24)).timestamp())

        logger.info(f"Attempting to created a new shorturl :: short_url_id : {short_url_id} :: created_at : {created_at} :: expires_at {expires_at}")

        created_data = self.shortener_repository.put_item_to_table(pk=short_url_id, data={"long_url": long_url, "user": "admin", "created_at": created_at, "expires_at": expires_at})

        if created_data is None or (created_data.get("ResponseMetadata").get("HTTPStatusCode") != 200):
            logger.error("Error while inserting data to dynamodb")
            raise Exception("Failed to insert data to database")

        if os.getenv("ENVIRONMENT") == "dev":
            short_url =  f"http://localhost:4003/{short_url_id}"
        else:
            short_url =  os.getenv("DOMAIN") + f"/{short_url_id}"

        logger.info(f"Generate short url :: {short_url}")

        return CreateShortUrlResponse(url=short_url)

    def update_short_url(self, params: dict, background_tasks: BackgroundTasks):
        short_url_id, long_url = params["short_url_id"], params["url"]

        logger.info(f"Attempting to update {short_url_id} - long_url to ${long_url}")

        result = self.shortener_repository.update_param_in_record(short_url_id, "long_url", long_url, "ALL_NEW")

        if result is None:
            logger.error("Short url id not found in db")
            raise Exception("Short url id not found or Error occurred while updating the url")

        logger.info(f"Successfully updated the url record for short_url_id {short_url_id}")

        new_long_url = result["Attributes"].get("long_url", None)
        if new_long_url is not None:
            attributes: KafkaProducerMessage = {
                "key": "UPDATE_URL",
                "value": {
                    "short_url_id": short_url_id,
                    "long_url": new_long_url
                }
            }
            topic_name = os.getenv("KAFKA_TOPIC")
            background_tasks.add_task(self.kafka_producer.send_message, topic_name, attributes)

        return UpdateShortUrlResponse(short_url_id=short_url_id, long_url=new_long_url)

    def delete_short_url_record(self, short_url_id, background_tasks: BackgroundTasks):
        logger.info(f"Attempting to delete the short url id {short_url_id}")
        result = self.shortener_repository.delete_record_from_table(short_url_id, return_values="ALL_OLD")

        if result.get("ResponseMetadata").get("HTTPStatusCode") != 200 or result.get("Attributes") is None or len(result.get("Attributes")) == 0:
            raise Exception("Error occurred while deleting data from db")

        logger.info(f"Successfully deleted the url record :: {short_url_id}")

        attributes: KafkaProducerMessage = {
            "key": "DELETE_URL",
            "value": {
                "short_url_id": short_url_id
            }
        }
        topic_name = os.getenv("KAFKA_TOPIC")
        background_tasks.add_task(self.kafka_producer.send_message, topic_name, attributes)

