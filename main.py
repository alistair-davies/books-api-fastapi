# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()
db_file = "books.db"

class BookData(BaseModel):
    title: str
    author: str

def get_connection():
    """Create a database connection and return rows as dictionaries."""
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def home():
    """Simple health check endpoint."""
    return {"message": "Book API running"}

@app.get("/books")
def get_books():
    """Return all books in the database."""
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM books")

        rows = cursor.fetchall()

    return [dict(row) for row in rows]



@app.get("/books/{book_id}")
def get_single_book(book_id: int):
    """Return a single book by its ID."""
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))

        book = cursor.fetchone()

    if book is None:
        raise HTTPException(
            status_code = 404,
            detail = "Book not found"
        )
    
    return dict(book)

@app.post("/books")
def add_book(book: BookData):
    """Add a new book to the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Check for existing book
        cursor.execute(
            """
            SELECT * FROM books
            WHERE title = ? AND author = ?
            """,
            (book.title, book.author)
        )

        existing_book = cursor.fetchone()

        if existing_book: 
            raise HTTPException(
                status_code = 409,
                detail = "Book already exists in database"
            )

        # Insert new book 
        cursor.execute(
            """
            INSERT INTO books (title, author)
            VALUES (?, ?)""", 
            (book.title, book.author)
        )

        conn.commit()

    return {"message": "Book added"}

@app.put("/books/{book_id}")
def update_book(book_id: int, book: BookData):
    """Update an existing book by ID."""
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE books
            SET title = ?, author = ?
            WHERE id = ?
            """,
            (book.title, book.author, book_id)
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code = 404,
                detail = "Book not found"
            )

        conn.commit()
    return {"message": "Book updated"}

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    """Delete a book by its ID."""
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM books WHERE id = ?",
            (book_id,)
        )

        # Check whether anything was deleted
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code = 404,
                detail = "Book not found"
            )

        conn.commit()

    return {"message": "Book deleted"}