from shortener_strategies.abstract_shortener import AbstractShortener


class Shortener:
    def __init__(self, shortener: AbstractShortener):
        self.shortener = shortener

    def get_short_id(self, data):
        return self.shortener.get_shortened_url_id(str(data))