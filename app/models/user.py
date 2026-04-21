from pydantic import BaseModel
from typing import Optional

class LoginPayload(BaseModel):
    username: str
    password: str