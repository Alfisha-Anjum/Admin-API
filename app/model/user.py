from pydantic import BaseModel

class Admin(BaseModel):
    full_name: str
    email: str
    mobile: int
    password: str
