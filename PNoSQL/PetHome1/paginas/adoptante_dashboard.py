import streamlit as st
from db import get_collection


def adoptante_dashboard():
    st.title("Panel del Adoptante 🐾")
    st.write("Bienvenido a PetHome. Explora nuestras mascotas y productos.")

    # Métricas de disponibilidad
    col1, col2 = st.columns(2)
    mascotas_disp = get_collection("Mascotas").count_documents({"disponible": True})
    productos_disp = get_collection("Productos").count_documents({"stock": {"$gt": 0}})
    with col1:
        st.metric("Mascotas disponibles", mascotas_disp)
    with col2:
        st.metric("Productos disponibles", productos_disp)

    st.markdown("---")
    st.info("Usa el menú lateral para navegar a ""Mascotas"" o ""Productos"".")