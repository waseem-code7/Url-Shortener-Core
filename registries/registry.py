import threading

from starlette.requests import Request

from services.shortUrlService import ShortUrlService
from services.shortener import Shortener
from strategies.base62 import Base62Strategy

SHORTENER_URL_SERVICE = "SHORTENER_URL_SERVICE"

class ServiceRegistry:
    __cache = {}
    __instance = None




