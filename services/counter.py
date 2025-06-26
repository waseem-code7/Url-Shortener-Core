import os
import threading

from common.utils import get_logger
from services.zookeeper import ZookeeperService

logger = get_logger(__name__)

# Strict Singleton class
class CounterService:
    __instance = None
    __lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    cls.__instance = super().__new__(cls)
                    cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self, zkService: ZookeeperService):
        if self.__initialized:
            return

        self.range = int(os.getenv("COUNTER_RANGE"))
        self._start = 0
        self._end = 0
        self.current = 0
        self.zkService = zkService
        self.lock = threading.Lock()
        self.__initialized = True

    def set_counter_attributes(self, node_path):
        node_sequence_number = int(node_path.split("-")[-1])
        self._start = node_sequence_number * self.range
        self._end = self._start + self.range - 1
        self.current = self._start

    def get_start(self):
        return self._start

    def get_end(self):
        return self._end

    def get_current(self):
        return self.current

    def get_counter_value_safe(self, retries = 2):
        if retries < 0:
            raise Exception("Unable to increment counter")

        # critical section
        with self.lock:
            value = self.current + 1

            if value < self._end:
                self.current += 1
                return value

            logger.warning("Counter Exhausted, calling zookeeper to create new ephemeral sequential node")
            path = self.zkService.create_new_node()
            self.set_counter_attributes(path)
            return self.get_counter_value_safe(retries - 1)



