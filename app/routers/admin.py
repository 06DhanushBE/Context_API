from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import models, schemas, utils
from app.database import get_db
from app.dependencies import verify_admin_key

router = APIRouter(prefix="/admin", dependencies=[Depends(verify_admin_key)])

@router.post("/keys", response_model=schemas.ApiKeyWithPlainKey)
async def create_api_key(
    key_data: schemas.ApiKeyCreate,
    db: AsyncSession = Depends(get_db)
):
    # Generate a new API key
    plain_key = utils.generate_api_key()
    key_hash = utils.hash_api_key(plain_key)
    
    db_key = models.ApiKey(
        name=key_data.name,
        key_hash=key_hash
    )
    db.add(db_key)
    await db.commit()
    await db.refresh(db_key)
    
    # Return the plain key only once
    return schemas.ApiKeyWithPlainKey(
        id=db_key.id,
        name=db_key.name,
        is_active=db_key.is_active,
        created_at=db_key.created_at,
        plain_key=plain_key
    )

@router.get("/keys", response_model=list[schemas.ApiKeyResponse])
async def list_api_keys(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(models.ApiKey))
    keys = result.scalars().all()
    return keys

@router.delete("/keys/{key_id}")
async def delete_api_key(
    key_id: int,
    db: AsyncSession = Depends(get_db)
):
    key = await db.get(models.ApiKey, key_id)
    if not key:
        raise HTTPException(status_code=404, detail="Key not found")
    
    # For now, soft delete (set inactive) or hard delete
    # We'll hard delete for simplicity; cascade deletion will be handled later.
    await db.delete(key)
    await db.commit()
    return {"message": "Key deleted"}
