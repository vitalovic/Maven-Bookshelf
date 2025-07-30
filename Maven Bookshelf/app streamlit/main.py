import pandas as pd 
import numpy as np
import streamlit as st
import table_sql
from sidebar import setup_layout_and_sidebar

setup_layout_and_sidebar()



books = table_sql.books
genres = table_sql.genres



cols = st.columns([1, 1, 1])  # La prima colonna è più stretta (1 su 5 parti totali)


choice_genres = genres['genres'].dropna().unique()
with cols[0]:  # Inserisci il filtro solo nella colonna stretta
    scelta_genere = st.multiselect("Genres", options=sorted(choice_genres), default=[])


choice_author = books['author'].dropna().unique()
with cols[1]:  # Inserisci il filtro solo nella colonna stretta
    scelta_autore = st.multiselect("Author", options=sorted(choice_author), default=[])



# Filtro per generi (se la lista non è vuota)
if scelta_genere:
    # Filtra i libri che contengono almeno uno dei generi scelti (case insensitive)
    # Qui applichiamo str.contains per ogni genere e poi facciamo l'OR
    filtro = books["genres"].apply(lambda x: any(gen.lower() in x.lower() for gen in scelta_genere) if isinstance(x, str) else False)
    books = books[filtro]


# Filtro per autori (se la lista non è vuota)
if scelta_autore:
    # Prendo solo i libri il cui autore è in lista scelta_autore
    books = books[books["author"].isin(scelta_autore)]


with cols[2]:
    rating = st.slider("Select the rating", min_value= 1, max_value= 5, value = 5)
    books = books[books['avg_rating'] <= rating]



st.write("Total Books:", books["work_id"].count())



# Rinomina colonne se necessario per chiarezza
books = books.rename(columns={
    "work_id":"ID",
    "image_url": "Cover",
    "original_title": "Title",
    "author": "Author",
    "original_publication_year": "Anno",
    "num_pages": "Pages",
    "reviews_count": "Reviews",
    "ratings_count": "Ratings",
    "avg_rating": "Avg Rating 5⭐",
    "genres": "Genres"
})


# CONFIGURAZIONE delle colonne speciali
config = {
    "Cover": st.column_config.ImageColumn(label="Cover", width="small"),
}

columns = ["Cover", "Title", "Author", "Anno", "Pages", "Reviews", "Ratings", "Avg Rating 5⭐", "Genres"]

st.data_editor(books[columns], column_config=config, use_container_width=True, height=800, disabled=True)