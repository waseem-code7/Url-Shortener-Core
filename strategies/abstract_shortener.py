from abc import ABC, abstractmethod

class AbstractShortener(ABC):

    """
    The function get_shortened_url_id needs to return a unique alphanumeric id.
    This id is then used to create shorturl.
    For Ex: if id = a1b2c3 then your short url will be - https://mydomain.com/a1b2c3

    Returns:
        str: unique short url id.
    """
    @abstractmethod
    def get_shortened_url_id(self, data: str) -> str:
        pass

