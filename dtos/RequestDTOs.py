from pydantic import BaseModel

class CreateShortUrlRequest(BaseModel):
    url: str

class UpdateShortUrlRequest(BaseModel):
    short_url_id: str
    url: str


