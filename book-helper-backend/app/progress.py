from fastapi import APIRouter
from app.schemas import ProgressUpdate

router = APIRouter()
user_progress = {}  # Global user reading progress

@router.post("/")
async def update_progress(progress: ProgressUpdate):
    user_books = user_progress.setdefault(progress.user_id, {})
    pages = user_books.setdefault(progress.book_id, set())
    pages.update(progress.pages_read)
    return {"message": "Progress updated", "pages_read_count": len(pages)}
