from pydantic import BaseModel

class CreateShortUrlResponse(BaseModel):
    url: str

class UpdateShortUrlResponse(BaseModel):
    short_url_id: str
    long_url: str


