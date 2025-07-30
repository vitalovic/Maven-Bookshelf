import pandas as pd
import streamlit as st
from sidebar import setup_layout_and_sidebar
import table_sql    


setup_layout_and_sidebar()

books = table_sql.books
similarBooks = table_sql.similarBooks
reviews = table_sql.reviews

idW = 0

cols = st.columns([1,1,1])

with cols[0]:
    TitleBooks = st.selectbox(label="Insert Title", options=list(books['original_title'].unique()), 
                              placeholder= 'Title', index=None)
   


cols = st.columns([0.5, 2])

with cols[0]:
    books = books[books['original_title']==TitleBooks]
    if not books.empty:
        st.image(books["image_url"].values[0], width=200)

with cols[1]:
    if not books.empty:
        st.subheader(f"{books['original_title'].values[0]}")
        st.write(f"Author: {books['author'].values[0]}")
        st.write(f"Published: {books['original_publication_year'].values[0]}")
        st.write(f"{books['avg_rating'].values[0]} ⭐ - {books['ratings_count'].values[0]} Ratings")
        st.write(f'{books["text_reviews_count"].values[0]}💭 - Reviews', )
        st.write(f"{books['description'].values[0]}")

        workID = books['work_id'].values[0]
        workName = books['original_title'].values[0]
        workAuthor = books['author'].values[0]
        workImg = books['image_url'].values[0]

        idW = workID
    
        if st.button("Add book to list"):
            nuovo_dato = pd.DataFrame([[workImg, workName, workAuthor]], columns=['Cover', 'Title', 'Author'])
            st.session_state.df = pd.concat([st.session_state.df, nuovo_dato], ignore_index=True)

    

 
        # Inizializzazione del DataFrame nella sessione
        if "df" not in st.session_state:
            st.session_state.df = pd.DataFrame(columns=['Cover', 'Title', 'Author',])
        
        
        # Mostra il DataFrame aggiornato
        if not st.session_state.df.empty:
            st.header("List of books")
            config = {"Cover": st.column_config.ImageColumn(label="Cover", width="small"),}
            st.data_editor(st.session_state.df, column_config=config, disabled=True)
            csv_bytes = st.session_state.df.to_csv(index=False).encode('utf-8')
            if st.download_button(label="Download list.csv", data=csv_bytes, file_name="list.csv", mime="text/csv"):
                st.session_state.df.to_csv("list.csv")



        imgSimilarBooks = similarBooks[similarBooks['original_work'] == workID].reset_index()


        if not imgSimilarBooks.empty:
            
            imgSimilarBooks = imgSimilarBooks.rename(columns={'Avg_Rating':'Avg Rating 5⭐'})
            st.header("Similar Books")
            # CONFIGURAZIONE delle colonne speciali
            config = {
                "Cover": st.column_config.ImageColumn(label="Cover", width="small"),
            }
            st.data_editor(imgSimilarBooks[['Cover', 'Title', 'Author', 'Avg Rating 5⭐']], column_config=config, disabled=True,  hide_index=True)




reviews_df = table_sql.reviews(idW)

if not reviews_df.empty: 
    st.header("Reviews 💭")
    reviews_df = reviews_df.rename(
                columns={
                    'date_added':  'Date',
                    'rating':      'Rating',
                    'review_text': 'Review',
                    'n_votes':     'Votes',
                    'n_comments':  'Comments',
                },
                errors='ignore'   # così non solleva eccezioni se manca qualche colonna
            )
    reviews_df['Date'] = pd.to_datetime(reviews_df['Date'], errors='coerce').dt.date
    st.data_editor(reviews_df[['Date', 'Rating', 'Review', 'Votes', 'Comments']].sort_values(by='Date'),  use_container_width=True, disabled = True, hide_index=True)
