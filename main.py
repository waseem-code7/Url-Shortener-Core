from contextlib import asynccontextmanager

from common.app_enums import AppState
from services.zookeeper import ZookeeperService
from fastapi import FastAPI
from common import utils
logger = utils.get_logger(__name__)

node_config = {
    "BASE_PATH": "/url-shortener/nodes",
    "RANGE_SIZE": 1000000
}

zkService = ZookeeperService(node_config.get("BASE_PATH"))

@asynccontextmanager
async def lifespan(app: FastAPI):

    node_config["APP_STATE"] = AppState.INITIALIZING
    node_path = zkService.connect()
    node_sequence_number = int(node_path.split("-")[-1])
    start = node_sequence_number * node_config.get("RANGE_SIZE")
    end = start + node_config.get("RANGE_SIZE") - 1
    node_config["START_COUNTER_VALUE"] = start
    node_config["END_COUNTER_VALUE"] = end
    node_config["APP_STATE"] = AppState.RUNNING
    
    yield

    node_config["APP_STATE"] = AppState.SHUTTING_DOWN
    logger.info("Server shutting down")
    zkService.close_conn()
    logger.info("closing zookeeper conn")

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health():
    return {"status": node_config.get("APP_STATE")}





