import sqlite3
import pandas as pd
import streamlit as st


# Connessione al database
conn = sqlite3.connect(r'goodreads.db')

books = pd.read_sql( """SELECT * FROM works ORDER BY original_title DESC""", conn)

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
    conn = sqlite3.connect(r"C:\Users\Davide\OneDrive\Desktop\Maven Bookshelf\database sql\goodreads.db")  # crea connessione nel thread corrente
    query = f"SELECT * FROM reviews WHERE work_id = {id}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Chiudere la connessione
conn.close()
