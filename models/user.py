from pydantic import BaseModel
from typing import Optional


class userModel(BaseModel):
    # id: Optional[int] = None # Optional 是设置可选
    username: str
    password: str


