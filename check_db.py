import sqlite3

with sqlite3.connect("books.db") as conn:

    cursor = conn.cursor()

    # Use this for getting contents of whole table 
    # cursor.execute("SELECT * FROM books")
    # rows = cursor.fetchall()
    # for row in rows:
    #     print(f"ID: {row[0]},  Title : {row[1]}, Author : {row[2]}")
        

    # ----------------------------------------------
    # Use this for finding the table information 
    # cursor.execute("PRAGMA table_info(books)")
    # rows = cursor.fetchall()
    # for row in rows:
    #     print(f"Column : {row[1]}, Type : {row[2]}")
    # ----------------------------------------------

    # --------------------------------------------------------------------
    # Use this to use the LIKE query 
    # cursor.execute("SELECT * FROM books WHERE title LIKE ?", ('D%',))
    # rows = cursor.fetchall()
    # for row in rows:
    #     print(row)
    # --------------------------------------------------------------------
    # Use this to check single column 
    cursor.execute("SELECT title FROM books")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
