from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from app.config import settings

admin_api_key_header = APIKeyHeader(name="X-Admin-Key", auto_error=False)

async def verify_admin_key(admin_key: str = Security(admin_api_key_header)):
    if not admin_key or admin_key != settings.ADMIN_KEY:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Invalid admin key"
        )
    return admin_key
