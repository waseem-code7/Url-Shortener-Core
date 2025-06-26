from strategies.abstract_shortener import AbstractShortener

class Base62Strategy(AbstractShortener):

    @staticmethod
    def encode(data: int) -> str:
        string = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

        short_id = ""

        while data > 0:
            ch = string[data % 62]
            short_id += ch
            data = data // 10

        return short_id

    def get_shortened_url_id(self, data: str) -> str:
        return self.encode(int(data))