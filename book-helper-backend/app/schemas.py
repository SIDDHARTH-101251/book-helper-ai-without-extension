from pydantic import BaseModel
from typing import List

class UploadResponse(BaseModel):
    book_id: str
    num_pages: int

class ProgressUpdate(BaseModel):
    user_id: str
    book_id: str
    pages_read: List[int]

class QueryRequest(BaseModel):
    user_id: str
    book_id: str
    question: str

class SummaryRequest(BaseModel):
    user_id: str
    book_id: str

class QueryResponse(BaseModel):
    answer: str