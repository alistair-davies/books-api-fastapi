import sqlite3

with sqlite3.connect("books.db") as conn:
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT
    )
    """)

    cursor.execute("""
    INSERT INTO books (title, author)
    VALUES ('Dune', 'Frank Herbert')
    """)

    cursor.execute("""
    INSERT INTO books (title, author)
    VALUES ('Foundation', 'Isaac Asimov')
    """)

print("Database created.")