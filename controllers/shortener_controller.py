from fastapi import APIRouter, Request, Depends, HTTPException, Body, BackgroundTasks

from common.dependencies import Authorization
from dtos.RequestDTOs import CreateShortUrlRequest, UpdateShortUrlRequest
from dtos.ResponseDTOs import UpdateShortUrlResponse, CreateShortUrlResponse
from registries.registry import ServiceRegistry
from services.short_url_service import ShortUrlService
from starlette import status

router = APIRouter(tags=["URL Shortener Routes"])

def get_short_url_service(request: Request) -> ShortUrlService:
    return ServiceRegistry.get_registry("SHORTENER_URL_SERVICE", request.app)


@router.post("/v1/shorturl", response_model=CreateShortUrlResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(Authorization.requires_login)])
def create_short_url(body: CreateShortUrlRequest = Body(), short_url_service: ShortUrlService = Depends(get_short_url_service)):
    try:
        short_url = short_url_service.create_new_short_url(body.url)
        return short_url
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.patch("/v1/shorturl", response_model=UpdateShortUrlResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(Authorization.requires_login)])
def update_short_url(background_tasks: BackgroundTasks, body: UpdateShortUrlRequest = Body(), short_url_service: ShortUrlService = Depends(get_short_url_service)):
    try:
        params = {
            "short_url_id": body.short_url_id,
            "url": body.url
        }
        return short_url_service.update_short_url(params, background_tasks)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/v1/shorturl/{short_url_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(Authorization.requires_login)])
def delete_short_url(background_tasks: BackgroundTasks, short_url_id, short_url_service: ShortUrlService = Depends(get_short_url_service)):
    try:
        return short_url_service.delete_short_url_record(short_url_id, background_tasks)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
