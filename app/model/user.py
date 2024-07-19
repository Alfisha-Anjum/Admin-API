from pydantic import BaseModel

class Admin(BaseModel):
    first_name: str
    last_name: str
    email: str
    mobile: int
    password: str
