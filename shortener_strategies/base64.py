import base64

from shortener_strategies.abstract_shortener import AbstractShortener


class Base64Strategy(AbstractShortener):

    def get_shortened_url_id(self, data: str) -> str:
        return base64.b64encode(data.encode('utf-8')).decode("utf-8")
