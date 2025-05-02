import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from common.config import get_app_status
from services.counter import CounterService
from services.zookeeper import ZookeeperService
from fastapi import FastAPI
from common import utils
logger = utils.get_logger(__name__)

load_dotenv()

zkService = ZookeeperService(os.getenv("BASE_PATH"))
counterService = CounterService(zkService)

from controllers.shortener_controller import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    zkService.connect()
    node_path = zkService.create_new_node()
    counterService.set_counter_attributes(node_path)
    app.state.counter_service = counterService
    app.state.zk_service = zkService
    yield
    logger.info("Server shutting down")
    zkService.close_conn()
    logger.info("closing zookeeper conn")

app = FastAPI(lifespan=lifespan)
app.include_router(router)

@app.get("/health")
async def health():
    return get_app_status(counterService, zkService)





