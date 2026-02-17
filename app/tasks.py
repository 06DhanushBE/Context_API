from app.celery_app import celery_app

@celery_app.task
def process_pdf(file_path: str, api_key_id: int, filename: str):
    # This will later: load PDF, chunk, embed, store in Qdrant
    return {"status": "success", "message": f"Processed {filename}"}
