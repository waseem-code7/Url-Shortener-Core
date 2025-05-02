from fastapi import APIRouter, Body, Request, Depends

from services.counter import CounterService
from services.shortener import Shortener
from strategies.base64 import Base64Encoder

router = APIRouter()

shortener_service = Shortener(Base64Encoder())

def get_counter_service(request: Request) -> CounterService:
    return request.app.state.counter_service


@router.post("/v1/shorturl")
async def create_short_url(counter_service=Depends(get_counter_service)):
    url_id = counter_service.get_counter_value_safe(2)
    return shortener_service.get_short_id(url_id)

@router.patch("/v1/shorturl")
async def update_short_url():
    pass

@router.delete("/v1/shorturl")
async def delete_short_url():
    pass