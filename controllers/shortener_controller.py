from fastapi import APIRouter

router = APIRouter()

@router.post("/v1/shorturl")
async def create_short_url():
    pass

@router.patch("/v1/shorturl")
async def update_short_url():
    pass

@router.delete("/v1/shorturl")
async def delete_short_url():
    pass