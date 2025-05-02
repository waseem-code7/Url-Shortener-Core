from contextlib import asynccontextmanager
from typing import Counter

from common.app_enums import AppState
from services.counter import CounterService
from services.zookeeper import ZookeeperService
from fastapi import FastAPI
from common import utils
logger = utils.get_logger(__name__)

node_config = {
    "BASE_PATH": "/url-shortener/nodes",
    "RANGE_SIZE": 1000000
}

zkService = ZookeeperService(node_config.get("BASE_PATH"))
counterService = CounterService(zkService)

@asynccontextmanager
async def lifespan(app: FastAPI):

    node_config["APP_STATE"] = AppState.INITIALIZING
    zkService.connect()
    node_path = zkService.create_new_node()
    counterService.set_counter_attributes(node_path)
    
    yield

    node_config["APP_STATE"] = AppState.SHUTTING_DOWN
    logger.info("Server shutting down")
    zkService.close_conn()
    logger.info("closing zookeeper conn")

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health():
    return {"status": node_config.get("APP_STATE")}





