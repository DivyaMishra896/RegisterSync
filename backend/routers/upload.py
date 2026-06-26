import os
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.circular import Circular
from services.pdf_parser import process_pdf
from config import settings

router = APIRouter(prefix="/api/upload", tags=["Upload"])


@router.post("")
async def upload_circular(
    file: UploadFile = File(...),
    source: str = "RBI",
    db: Session = Depends(get_db)
):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    file_bytes = await file.read()

    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty file uploaded")

    try:
        result = process_pdf(file_bytes)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Failed to parse PDF: {str(e)}")

    circular = Circular(
        filename=file.filename,
        source=source,
        raw_text=result["cleaned_text"],
        status="uploaded"
    )
    db.add(circular)
    db.commit()
    db.refresh(circular)

    upload_path = os.path.join(settings.UPLOAD_DIR, f"{circular.id}_{file.filename}")
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    with open(upload_path, "wb") as f:
        f.write(file_bytes)

    return {
        "message": "Circular uploaded successfully",
        "circular_id": circular.id,
        "filename": file.filename,
        "text_length": result["total_chars"],
        "num_chunks": result["num_chunks"],
        "status": "uploaded"
    }


@router.get("/circulars")
async def list_circulars(db: Session = Depends(get_db)):
    circulars = db.query(Circular).order_by(Circular.upload_date.desc()).all()
    return {"circulars": [c.to_dict() for c in circulars]}


@router.get("/circulars/{circular_id}")
async def get_circular(circular_id: int, db: Session = Depends(get_db)):
    circular = db.query(Circular).filter(Circular.id == circular_id).first()
    if not circular:
        raise HTTPException(status_code=404, detail="Circular not found")
    return circular.to_dict()
