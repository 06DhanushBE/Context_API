from fastapi import HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from starlette.status import HTTP_401_UNAUTHORIZED
from app.database import get_db
from app.models import ApiKey
from app.utils import verify_api_key

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_current_api_key(
    api_key: str = Security(api_key_header),
    db: AsyncSession = Depends(get_db)
):
    if not api_key:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Missing API key"
        )
    
    result = await db.execute(
        select(ApiKey).where(ApiKey.is_active == True)
    )
    keys = result.scalars().all()
    
    for key in keys:
        if verify_api_key(api_key, key.key_hash):
            return key
    
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Invalid API key"
    )
