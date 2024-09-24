from pydantic import BaseModel

class Admin(BaseModel):
    full_name: str
    email: str
    mobile: int
    password: str

class Login(BaseModel):
    email: str
    password: str

class Yaseen(BaseModel):
    full_name: str
    email: str
    message: str