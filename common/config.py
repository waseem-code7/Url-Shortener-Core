import os

from services.counter import CounterService
from services.zookeeper import ZookeeperService
from sessions.config import SessionConfig


def get_app_status(counter: CounterService, zk: ZookeeperService):
    APP_INFO = {
        "base_path": os.getenv("BASE_PATH"),
        "counter_range": os.getenv("COUNTER_RANGE"),
        "start": counter.get_start(),
        "end": counter.get_end(),
        "current": counter.get_current(),
        "zookeeper_connected": zk.is_zookeeper_connected()
    }
    return APP_INFO

def get_session_config() -> SessionConfig:
    return SessionConfig()