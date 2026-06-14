from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from datetime import datetime



class User(Document):
    username: str = Field(min_length=3, max_length=50)
    password: str
    email: str

    created: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "user"
            

class RegisterUser(BaseModel):
    username: str
    password: str
    email: str


class LoginUser(BaseModel):
    username: str
    password: str


class CurrentUser(BaseModel):
    username: str
    email: str
    id: PydanticObjectId
