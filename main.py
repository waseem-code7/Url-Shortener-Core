import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from common.config import get_app_status, get_session_config
from services.counter import CounterService
from services.kafka import KafkaProducer
from services.zookeeper import ZookeeperService
from fastapi import FastAPI
from common import utils
from sessions.core import SessionManager
from sessions.middleware import SessionMiddleware

logger = utils.get_logger(__name__)

load_dotenv()

zkService = ZookeeperService(os.getenv("BASE_PATH"))
counterService = CounterService(zkService)
kafkaProducer = KafkaProducer()
sessionManager = SessionManager(config=get_session_config())

from controllers.shortener_controller import router as shortener_router
from controllers.auth import router as auth_router
from controllers.user import router as user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    zkService.connect()
    node_path = zkService.create_new_node()
    counterService.set_counter_attributes(node_path)
    app.state.counter_service = counterService
    app.state.zk_service = zkService
    await kafkaProducer.start_producer()
    app.state.kafka_producer = kafkaProducer
    yield
    logger.info("Server shutting down")
    app.state.kafkaProducer.stop_producer()
    zkService.close_conn()
    logger.info("closing zookeeper conn")

app = FastAPI(lifespan=lifespan)

# Middleware

app.add_middleware(SessionMiddleware, sessionManager)

# Routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(shortener_router)

@app.get("/health")
async def health():
    return get_app_status(counterService, zkService)





