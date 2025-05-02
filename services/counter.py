import os
from common.utils import get_logger
from services.zookeeper import ZookeeperService

logger = get_logger(__name__)

# Strict Singleton class
class CounterService:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
            cls.initialized = False
        return cls.instance

    def __init__(self, zkService: ZookeeperService):
        if not self.__class__.initialized:
            self.__class__.initialized = True
            self.range = int(os.getenv("COUNTER_RANGE"))
            self._start = 0
            self._end = 0
            self.current = 0
            self.zkService = zkService

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

        value = self.current + 1

        if value < self._end:
            self.current += 1
            return value

        logger.warn("Counter Exhausted, calling zookeeper to create new ephemeral sequential node")
        path = self.zkService.create_new_node()
        self.set_counter_attributes(path)
        return self.get_counter_value_safe(retries - 1)



