from fastapi import APIRouter, Request, Depends, HTTPException, Body
from fastapi.concurrency import run_in_threadpool

from dtos.RequestDTOs import CreateShortUrlRequest, UpdateShortUrlRequest
from services.shortUrlService import ShortUrlService
from services.shortener import Shortener
from strategies.base62 import Base62Strategy
from starlette import status

router = APIRouter()

def get_short_url_service(request: Request) -> ShortUrlService:
    counter_service = request.app.state.counter_service
    shortener_service = Shortener(Base62Strategy())
    return ShortUrlService(counter_service, shortener_service)


@router.post("/v1/shorturl")
def create_short_url(body: CreateShortUrlRequest = Body(), short_url_service: ShortUrlService = Depends(get_short_url_service)):
    try:
        short_url = short_url_service.create_new_short_url(body.url)
        return short_url
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.patch("/v1/shorturl")
def update_short_url(body: UpdateShortUrlRequest = Body(), short_url_service: ShortUrlService = Depends(get_short_url_service)):
    try:
        params = {
            "short_url_id": body.short_url_id,
            "url": body.url
        }
        return short_url_service.update_short_url(params)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/v1/shorturl/{short_url_id}")
def delete_short_url(short_url_id, short_url_service: ShortUrlService = Depends(get_short_url_service)):
    try:
        return short_url_service.delete_short_url_record(short_url_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
