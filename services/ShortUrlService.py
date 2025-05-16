import os

from services.counter import CounterService
from services.shortener import Shortener
from repository.shortener import ShortenerRepository
from datetime import datetime, timezone, timedelta
from common import utils
logger = utils.get_logger("ShortUrlService.py")


class ShortUrlService:

    def __init__(self, counter_service: CounterService, shortener: Shortener):
        self.counter_service = counter_service
        self.shortener = shortener
        self.shortener_repository = ShortenerRepository(os.getenv("DYNAMO_URL_TABLE_NAME"))


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
            return f"http://localhost:4002/{short_url_id}"

        return os.getenv("DOMAIN") + f"/{short_url_id}"

    def update_short_url(self, params: dict):
        short_url_id, long_url = params["short_url_id"], params["url"]
        result = self.shortener_repository.update_param_in_record(short_url_id, "long_url", long_url, "ALL_NEW")
        if result is None:
            logger.error("Short url id not found in db")
            raise Exception("Short url id not found or Error occurred while updating the url")
        logger.info("Successfully updated the url record")
        return result["Attributes"]

    def delete_short_url_record(self, short_url_id):
        logger.info("Attempting to delete the short url id")
        return self.shortener_repository.delete_record_from_table(short_url_id)

