import streamlit as st
from db import get_collection
from datetime import date


def cuidados_adoptante():
    st.header("Registrar Cuidado 🏥")
    # Obtener mascotas adoptadas por el usuario
    adopciones = get_collection("Adopciones").find({"user": st.session_state.user['username']})
    pets = [a['mascota'] for a in adopciones]
    if not pets:
        st.info("No has adoptado ninguna mascota aún.")
        return

    with st.form("cuidado_form"):
        mascota = st.selectbox("Selecciona tu mascota", pets)
        descripcion = st.text_area("Descripción del cuidado realizado")
        fecha = st.date_input("Fecha del cuidado", date.today())
        if st.form_submit_button("Registrar Cuidado"):
            get_collection("Cuidados").insert_one({
                "user": st.session_state.user['username'],
                "mascota": mascota,
                "descripcion": descripcion,
                "fecha": fecha.isoformat()
            })
            st.success("Cuidado registrado correctamente.")