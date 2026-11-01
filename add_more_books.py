import sqlite3

# Connect to the database
with sqlite3.connect("books.db") as conn:

    # Create a cursor
    cursor = conn.cursor()

    # Add 2 books
    cursor.execute(
            "INSERT INTO books (title, author) VALUES (?, ?)",
            ("Moby-Dick", "Hermann Melville")
    )

    cursor.execute(
            "INSERT INTO books (title, author) VALUES (?, ?)",
            ("Animal Farm", "George Orwell")
    )

    # Save changes
    conn.commit()

print("Books added successfully")
