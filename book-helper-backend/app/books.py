from fastapi import APIRouter, UploadFile, File, HTTPException
from app.pdf_service import extract_text_by_page
from app.embedding_service import get_embedding
from app.schemas import UploadResponse
import os
import uuid

router = APIRouter()
UPLOAD_DIR = "./uploaded_books"
os.makedirs(UPLOAD_DIR, exist_ok=True)

books = {}  # Global book storage

@router.post("/", response_model=UploadResponse)
async def upload_book(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    book_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{book_id}.pdf")

    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    pages_text = extract_text_by_page(file_path)
    pages_embeddings = [get_embedding(text) for text in pages_text]

    books[book_id] = {
        "filename": file.filename,
        "pages_text": pages_text,
        "pages_embeddings": pages_embeddings,
    }

    return UploadResponse(book_id=book_id, num_pages=len(pages_text))
