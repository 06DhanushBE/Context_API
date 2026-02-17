from fastapi import FastAPI
from app.database import engine, Base
from app.routers import admin, user

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def root():
    return {"message": "RAG-as-a-Service API"}

app.include_router(admin.router)
app.include_router(user.router)