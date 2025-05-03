from fastapi import APIRouter, Request, Depends, HTTPException, Body

from dtos.RequestDTOs import CreateShortUrlRequest
from services.ShortUrlService import ShortUrlService
from services.shortener import Shortener
from strategies.base64 import Base64Encoder
from starlette import status

router = APIRouter()



def get_short_url_service(request: Request) -> ShortUrlService:
    counter_service = request.app.state.counter_service
    shortener_service = Shortener(Base64Encoder())
    return ShortUrlService(counter_service, shortener_service)



@router.post("/v1/shorturl")
async def create_short_url(body: CreateShortUrlRequest = Body(), short_url_service: ShortUrlService = Depends(get_short_url_service)):
    try:
        return short_url_service.create_new_short_url(body.url)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.patch("/v1/shorturl")
async def update_short_url():
    pass

@router.delete("/v1/shorturl")
async def delete_short_url():
    pass