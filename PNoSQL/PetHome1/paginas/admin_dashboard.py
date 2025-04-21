import streamlit as st
from db import get_collection
from paginas import (
    mascotas_crud, productos_crud, usuarios_crud
)

def admin_dashboard():
    st.title("Panel de Administración 🛠️")
    st.write("Gestiona tu veterinaria PetHome desde aquí.")

    # Métricas clave
    col1, col2, col3 = st.columns(3)
    total_users = get_collection("Usuarios").count_documents({})
    total_mascotas = get_collection("Mascotas").count_documents({})
    total_productos = get_collection("Productos").count_documents({})
    with col1:
        st.metric("Usuarios totales", total_users)
    with col2:
        st.metric("Mascotas registradas", total_mascotas)
    with col3:
        st.metric("Productos registrados", total_productos)

    st.markdown("---")

    # Inicializar navegación si no existe
    if "menu_admin" not in st.session_state:
        st.session_state.menu_admin = None

    # Accesos rápidos a CRUDs
    tabs = st.tabs(["Usuarios", "Mascotas", "Productos"])
    with tabs[0]:
        if st.button("Ir a CRUD Usuarios"):
            st.session_state.menu_admin = "Usuarios"
    with tabs[1]:
        if st.button("Ir a CRUD Mascotas"):
            st.session_state.menu_admin = "Mascotas"
    with tabs[2]:
        if st.button("Ir a CRUD Productos"):
            st.session_state.menu_admin = "Productos"

    if st.session_state.get("menu_admin") == "Usuarios":
        usuarios_crud.usuarios_crud()
    elif st.session_state.get("menu_admin") == "Mascotas":
        mascotas_crud.mascotas_crud()
    elif st.session_state.get("menu_admin") == "Productos":
        productos_crud.productos_crud()