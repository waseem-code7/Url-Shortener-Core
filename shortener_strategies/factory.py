from shortener_strategies.abstract_shortener import AbstractShortener
from shortener_strategies.base62 import Base62Strategy
from shortener_strategies.base64 import Base64Strategy


class ShortenerFactory:

    @staticmethod
    def get_strategy(name: str) -> AbstractShortener:
        if name == "BASE_62":
            return Base62Strategy()
        if name == "BASE_64":
            return Base64Strategy()
        raise ValueError(f"No strategy available for given name '{name}'")