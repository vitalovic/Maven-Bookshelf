import sqlite3
import pandas as pd
import streamlit as st
import os



# Connessione al database
conn = sqlite3.connect(r'goodreads.db')


print("File esiste?", os.path.exists("goodreads.db"))
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(tables)

books = pd.read_sql( "SELECT * FROM works ORDER BY original_title DESC", conn)

colonne_intere = ["original_publication_year", "num_pages",  "reviews_count", "ratings_count"]
for col in colonne_intere:
    books[col] = books[col].apply(lambda x: str(int(x)) if pd.notnull(x) and isinstance(x, (int, float)) else x)


genres = pd.read_sql("SELECT * FROM genres", conn)

similarBooks = pd.read_sql("""
SELECT 
    sb.work_id AS original_work,
    sb.similar_books AS similar_work,
    w.original_title AS similar_title,
    w.image_url AS Cover,
    w.original_title AS Title,
    w.author AS Author,
    w.avg_rating AS Avg_Rating,
    w.genres AS Genres
FROM similarBooks AS sb
JOIN works AS w ON sb.similar_books = w.work_id;
""", conn)

def reviews(id):
    conn = sqlite3.connect("goodreads.db")  # crea connessione nel thread corrente
    query = f"SELECT * FROM reviews WHERE work_id = {id}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Chiudere la connessione
conn.close()
