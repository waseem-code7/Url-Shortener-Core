import os

from services.counter import CounterService
from services.shortener import Shortener
from repository.shortener import ShortenerRepository
from datetime import datetime


class ShortUrlService:

    def __init__(self, counter_service: CounterService, shortener: Shortener):
        self.counter_service = counter_service
        self.shortener = shortener
        self.shortener_repository = ShortenerRepository("Urls")


    def create_new_short_url(self, long_url):
        counter_val = self.counter_service.get_counter_value_safe(retries=2)
        short_url_id = self.shortener.get_short_id(counter_val)
        timestamp = int(datetime.utcnow().timestamp())
        created_data = self.shortener_repository.add_item_to_table(pk=short_url_id, sk=timestamp, data={"long_url": long_url, "user": "admin"})

        if created_data.get("ResponseMetadata").get("HTTPStatusCode") != 200:
            raise Exception("Error while inserting data to dynamodb")

        if os.getenv("ENVIRONMENT") == "dev":
            return f"http://localhost:4002/{short_url_id}"

        return os.getenv("DOMAIN") + f"/{short_url_id}"


