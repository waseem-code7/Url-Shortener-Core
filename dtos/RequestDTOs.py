from pydantic import BaseModel, EmailStr


class CreateShortUrlRequest(BaseModel):
    url: str

class UpdateShortUrlRequest(BaseModel):
    short_url_id: str
    url: str

class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str



