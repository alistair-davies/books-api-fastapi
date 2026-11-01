# main.py

from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    author: str

class BookCreate(BaseModel):
    title: str
    author: str


@app.get("/")
def home():
    return {"message" : "Book API running"}

@app.get("/books")
def get_books():
    with sqlite3.connect("books.db") as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM books")

        rows = cursor.fetchall()

    books = []

    for row in rows: 
        books.append({
            "id" : row[0],
            "title" : row[1],
            "author" : row[2]
        })
    return books

@app.get("/books/{book_id}")
def get_single_book(book_id: int):
    with sqlite3.connect("books.db") as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))

        book = cursor.fetchone()
    return book

@app.post("/books")
def add_book(book: BookCreate):
    with sqlite3.connect("books.db") as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO books (title, author)
            VALUES (?, ?)""", 
            (book.title, book.author)
        )

        conn.commit()

    return {"message" : "Book added"}

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    with sqlite3.connect("books.db") as conn:
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM books WHERE id = ?",
            (book_id,)
        )

        # Check whether anything was deleted
        if cursor.rowcount == 0:
            return {"error" : "Book not found"}

        conn.commit()

    return {"message" : "Book deleted"}