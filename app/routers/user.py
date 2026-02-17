from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.user_auth import get_current_api_key
from app.models import ApiKey
from app.tasks import process_pdf
import tempfile

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    api_key: ApiKey = Depends(get_current_api_key)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    task = process_pdf.delay(tmp_path, api_key.id, file.filename)
    
    return {"task_id": task.id, "status": "processing"}

@router.get("/task/{task_id}")
async def get_task_status(
    task_id: str,
    api_key: ApiKey = Depends(get_current_api_key)
):
    from celery.result import AsyncResult
    from app.celery_app import celery_app
    
    task = AsyncResult(task_id, app=celery_app)
    if task.failed():
        return {"status": "failed", "error": str(task.info)}
    elif task.successful():
        return {"status": "completed", "result": task.result}
    else:
        return {"status": task.state}
