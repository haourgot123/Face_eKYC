from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[str]
    user_name: str
    password: str
    full_name: str
    phone: str