from kazoo.client import KazooClient
from kazoo.exceptions import NodeExistsError
from common.utils import get_logger
logger = get_logger(__name__)

# Strict Singleton class
class ZookeeperService:

    def __init__(self, base_path):
        if not self.__class__.initialized:
            self.base_path: str = base_path
            self.zkClient: KazooClient = KazooClient()
            self.__class__.initialized = True

    def connect(self) -> str:
        try:
            self.zkClient.start()
            logger.info("Connecting to ZooKeeper...")
            self.zkClient.ensure_path(self.base_path)
            path = self.zkClient.create(path=self.base_path  + "/node-", ephemeral=True, sequence=True)
            logger.info(f"Successfully created ephemeral sequential node at : {path}")
            return path
        except NodeExistsError:
            logger.warning(f"Znode already exists at {self.base_path}")
        except Exception as e:
            logger.error(f"Error connecting to ZooKeeper: {e}")

    def close_conn(self):
        try:
            if self.zkClient:
                self.zkClient.stop()
                self.zkClient.close()
                logger.info("ZooKeeper connection closed.")
        except Exception as e:
            logger.error(f"Error closing ZooKeeper connection: {e}")

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
            cls.initialized = False
        return cls.instance



