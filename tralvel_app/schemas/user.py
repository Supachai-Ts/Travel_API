from pydantic import BaseModel

class UserCreate(BaseModel):
    firstname: str
    lastname: str
    age: int
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
