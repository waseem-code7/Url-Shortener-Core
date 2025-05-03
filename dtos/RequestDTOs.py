from pydantic import BaseModel

class CreateShortUrlRequest(BaseModel):
    url: str