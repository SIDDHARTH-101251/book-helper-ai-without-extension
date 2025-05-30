from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.query import router as query_router
from app.books import router as books_router
from app.progress import router as progress_router

app = FastAPI(title="Book AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["chrome-extension://inbklbbjoppgedfplioapdffhajlnide"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books_router, prefix="/books", tags=["Books"])
app.include_router(progress_router, prefix="/progress", tags=["Progress"])
app.include_router(query_router, prefix="/query", tags=["Query & Summary"])

@app.get("/")
def root():
    return {"message": "Book AI backend is running!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
