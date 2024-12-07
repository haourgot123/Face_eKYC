from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[str]
    user_name: str
    password: str
    full_name: str
    phone: str


class Card(BaseModel):
    id: Optional[str]
    user_name: str
    so_cccd: str
    ho_ten: str
    ngay_sinh: str
    gioi_tinh: str
    quoc_tich: str
    que_quan: str
    thuong_tru: str
    ngay_cap: str
    noi_cap: str



    