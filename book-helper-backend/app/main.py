from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.query import router as query_router
from app.books import router as books_router
from app.progress import router as progress_router

app = FastAPI(title="📚 Book AI Backend")

# --- CORS Configuration ---
origins = [
    "chrome-extension://inbklbbjoppgedfplioapdffhajlnide",  # for Chrome extension if needed
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allow specified origins
    allow_credentials=True,           # Allow cookies/authorization headers
    allow_methods=["*"],              # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],              # Allow all headers
)

# --- Routers ---
app.include_router(books_router, prefix="/books", tags=["📘 Books"])
app.include_router(progress_router, prefix="/progress", tags=["📊 Progress"])
app.include_router(query_router, prefix="/query", tags=["🧠 Query & Summary"])

# --- Health Routes ---
@app.get("/", tags=["🌐 Root"])
def root():
    return {"message": "Book AI backend is running!"}

@app.get("/health", tags=["🌡️ Health Check"])
def health_check():
    return {"status": "ok"}