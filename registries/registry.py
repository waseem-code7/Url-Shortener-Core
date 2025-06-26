import os
import threading

from fastapi import FastAPI

from repository.shortener import ShortenerRepository
from repository.user import UserRepository
from services.auth import AuthService
from services.short_url_service import ShortUrlService
from services.shortener import Shortener
from services.user import UserService
from shortener_strategies.factory import ShortenerFactory

SHORTENER_URL_SERVICE = "SHORTENER_URL_SERVICE"
AUTH_SERVICE = "AUTH_SERVICE"
USER_SERVICE = "USER_SERVICE"

class ServiceRegistry:
    __cache = {}
    __lock = threading.Lock()

    @staticmethod
    def get_registry(registry_name, app: FastAPI = None, config=None):
        if registry_name == SHORTENER_URL_SERVICE and registry_name not in ServiceRegistry.__cache:
            with ServiceRegistry.__lock:
                if registry_name not in ServiceRegistry.__cache:
                    counter_service = app.state.counter_service
                    shortener_service = Shortener(ShortenerFactory.get_strategy(os.getenv("BASE_62")))
                    kafka_producer = app.state.kafka_producer
                    shortener_repository = ShortenerRepository("URL_DATA")
                    ServiceRegistry.__cache[SHORTENER_URL_SERVICE] = ShortUrlService(counter_service, shortener_service, kafka_producer, shortener_repository)

        elif registry_name == AUTH_SERVICE and registry_name not in ServiceRegistry.__cache:
            with ServiceRegistry.__lock:
                if registry_name not in ServiceRegistry.__cache:
                    user_repository = UserRepository("USER_DTA")
                    ServiceRegistry.__cache[USER_SERVICE] = AuthService(user_repository=user_repository)

        elif registry_name == USER_SERVICE and registry_name not in ServiceRegistry.__cache:
            with ServiceRegistry.__lock:
                if registry_name not in ServiceRegistry.__cache:
                    user_repository = UserRepository("USER_DTA")
                    ServiceRegistry.__cache[USER_SERVICE] = UserService(user_repository=user_repository)

        return ServiceRegistry.__cache.get(registry_name, None)











