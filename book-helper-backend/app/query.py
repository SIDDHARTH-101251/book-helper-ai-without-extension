from fastapi import APIRouter, HTTPException
from app.schemas import QueryRequest, SummaryRequest, QueryResponse
from app.embedding_service import get_embedding, search_similar_pages
from app.gemini_service import call_gemini_api
from app.books import books
from app.progress import user_progress

router = APIRouter()

@router.post("/", response_model=QueryResponse)
async def query_book(request: QueryRequest):
    user_books = user_progress.get(request.user_id, {})
    pages_read = user_books.get(request.book_id, set())
    if not pages_read:
        raise HTTPException(status_code=400, detail="No pages read yet.")

    book = books.get(request.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")

    # Get embeddings and text of pages user read
    pages_text = book["pages_text"]
    pages_embeddings = book["pages_embeddings"]

    read_pages = sorted(pages_read)
    read_texts = [pages_text[i] for i in read_pages if i < len(pages_text)]

    read_embeddings = [pages_embeddings[i] for i in read_pages]

    # Get query embedding
    query_emb = get_embedding(request.question)

    # Find top relevant pages among read pages
    top_page_indices_in_read = search_similar_pages(query_emb, read_embeddings, top_k=3)
    relevant_texts = [read_texts[i] for i in top_page_indices_in_read]

    prompt = f"""
    You are a helpful assistant. Based ONLY on the following parts of a book, answer the question below.

    Book excerpts:
    {"\n\n".join(relevant_texts)}

    Question:
    {request.question}
    """

    answer = call_gemini_api(prompt)
    return QueryResponse(answer=answer)


@router.post("/summary", response_model=QueryResponse)
async def summarize_book(request: SummaryRequest):
    user_books = user_progress.get(request.user_id, {})
    pages_read = user_books.get(request.book_id, set())
    if not pages_read:
        raise HTTPException(status_code=400, detail="No pages read yet.")

    book = books.get(request.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")

    read_text = "\n".join(
        book["pages_text"][i] for i in sorted(pages_read)
    )

    prompt = f"""
    You are a helpful assistant. Summarize the following book content in a concise and spoiler-free way:

    Content:
    {read_text}
    """

    answer = call_gemini_api(prompt)
    return QueryResponse(answer=answer)
