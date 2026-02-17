from pydantic import BaseModel
from datetime import datetime

class ApiKeyCreate(BaseModel):
    name: str

class ApiKeyResponse(BaseModel):
    id: int
    name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ApiKeyWithPlainKey(ApiKeyResponse):
    plain_key: str  # only returned once at creation