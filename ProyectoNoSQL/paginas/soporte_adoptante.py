import streamlit as st
from db import get_collection
from datetime import datetime


def soporte_adoptante():
    st.header("Soporte 🆘")
    with st.form("ticket_form"):
        asunto = st.text_input("Asunto del ticket")
        descripcion = st.text_area("Descripción del problema")
        if st.form_submit_button("Enviar Ticket"):
            get_collection("Soporte").insert_one({
                "user": st.session_state.user['username'],
                "asunto": asunto,
                "descripcion": descripcion,
                "estatus": "Abierto",
                "fecha": datetime.now().isoformat()
            })
            st.success("Ticket enviado con éxito.")