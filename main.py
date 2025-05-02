import os
from contextlib import asynccontextmanager

from services.counter import CounterService
from services.zookeeper import ZookeeperService
from fastapi import FastAPI
from common import utils
logger = utils.get_logger(__name__)

zkService = ZookeeperService(os.getenv("BASE_PATH"))
counterService = CounterService(zkService)

@asynccontextmanager
async def lifespan(app: FastAPI):
    zkService.connect()
    node_path = zkService.create_new_node()
    counterService.set_counter_attributes(node_path)
    yield
    logger.info("Server shutting down")
    zkService.close_conn()
    logger.info("closing zookeeper conn")

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health():
    return {"status": "OK"}





