import streamlit as st
from db import get_collection
from datetime import datetime


def comentarios_adoptante():
    st.header("Dejar Comentario 💬")
    with st.form("coment_form"):
        texto = st.text_area("Escribe tu comentario")
        if st.form_submit_button("Enviar Comentario"):
            get_collection("Comentarios").insert_one({
                "user": st.session_state.user['username'],
                "texto": texto,
                "fecha": datetime.now().isoformat()
            })
            st.success("¡Gracias por tu comentario!")