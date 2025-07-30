import streamlit as st

def setup_layout_and_sidebar():
    # Espandi layout della pagina
    st.set_page_config(layout="wide")

    # Rimuovi margini laterali eccessivi + nascondi menu automatico
    st.markdown("""
        <style>
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
            /* Nasconde il menu di navigazione automatico delle pagine */
            [data-testid="stSidebarNav"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)

    
    #Logo Goodreads
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Goodreads_logo_%282007%E2%80%932025%29.svg/2560px-Goodreads_logo_%282007%E2%80%932025%29.svg.png", width=300)

    # Sidebar fissa con logo e link
    with st.sidebar:
        # Logo Maven
        st.image("https://cdn.prod.website-files.com/661b25aa8bda4a590a431922/66db2771530c4c2e5c59eaeb_Maven%20Analytics%20DARK%20RGB.webp", width=200)

        # Creazione dei link nella sidebar
        st.page_link("main.py", label="Library", icon="🏠")
        st.page_link("pages/Similar_Books.py", label="Bookly", icon="📚")
        #st.page_link("pages/goodreads_stats.py", label="Stats Goodreads", icon="📊")

