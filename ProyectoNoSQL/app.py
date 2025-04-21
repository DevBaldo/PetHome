import streamlit as st
from auth import login_user, register_user
from paginas import (
    admin_dashboard, adoptante_dashboard, comentarios_adoptante, cuidados_adoptante, donaciones_adoptante,
    mascotas_crud, productos_crud, adopciones_crud, refugios_crud, donaciones_crud,
    comentarios_crud, cuidados_crud, soporte_adoptante, usuarios_crud, soporte_crud,
    productos_disponibles,
    adoptar, cart, historial
)

st.set_page_config(page_title="PetHome 🐾", layout="wide")
# Tema simple
st.markdown("""
<style>
  .sidebar .sidebar-content { background-color: #FAFAFA; }
  .block-container { padding: 2rem; }
  h1,h2,h3 { color: #2E7D32; }
</style>
""", unsafe_allow_html=True)

st.sidebar.image("logo.jpg", width=150)
st.sidebar.title("PetHome 🐾")

# Inicializar sesión
if "user" not in st.session_state:
    st.session_state.user = None

# Login / Registro
if st.session_state.user is None:
    
    choice = st.sidebar.selectbox("Acceso", ["Iniciar sesión", "Registrarse"])
    if choice == "Iniciar sesión":
        usuario = st.sidebar.text_input("Usuario")
        clave = st.sidebar.text_input("Contraseña", type="password")
        if st.sidebar.button("Entrar"):
            if login_user(usuario, clave):
                st.rerun()
            else:
                st.sidebar.error("Credenciales incorrectas")

    else:
        nuevo = st.sidebar.text_input("Nuevo usuario")
        clave2 = st.sidebar.text_input("Nueva contraseña", type="password")
        role = "adoptante"
        if st.sidebar.button("Registrarse"):
            ok, msg = register_user(nuevo, clave2, role)
            if ok:
                st.sidebar.success(msg)
            else:
                st.sidebar.error(msg)

# Panel principal
else:
    st.sidebar.write(f"👤 {st.session_state.user['username']}")
    st.sidebar.write(f"🔑 Rol: {st.session_state.user['role']}")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.clear()
        st.rerun()

    if st.session_state.user['role'] == 'admin':
        page = st.sidebar.selectbox("Menú Admin", [
            "Dashboard", "Mascotas", "Productos", "Adopciones",
            "Refugios", "Donaciones", "Comentarios", "Cuidados",
            "Usuarios", "Soporte"
        ])
        if page == "Dashboard": admin_dashboard.admin_dashboard()
        elif page == "Mascotas": mascotas_crud.mascotas_crud()
        elif page == "Productos": productos_crud.productos_crud()
        elif page == "Adopciones": adopciones_crud.adopciones_crud()
        elif page == "Refugios": refugios_crud.refugios_crud()
        elif page == "Donaciones": donaciones_crud.donaciones_crud()
        elif page == "Comentarios": comentarios_crud.comentarios_crud()
        elif page == "Cuidados": cuidados_crud.cuidados_crud()
        elif page == "Usuarios": usuarios_crud.usuarios_crud()
        elif page == "Soporte": soporte_crud.soporte_crud()

    else:
        page = st.sidebar.selectbox("Menú Adoptante", [
            "Dashboard", "Productos",
            "Adoptar", "Cuidados", "Comentarios", "Donaciones", "Carrito", "Historial",
            "Soporte"
        ])
        if page == "Dashboard": adoptante_dashboard.adoptante_dashboard()
        elif page == "Productos": productos_disponibles.productos_disponibles()
        elif page == "Adoptar": adoptar.adoptar_page()
        elif page == "Cuidados": cuidados_adoptante.cuidados_adoptante()
        elif page == "Comentarios": comentarios_adoptante.comentarios_adoptante()
        elif page == "Donaciones": donaciones_adoptante.donaciones_adoptante()
        elif page == "Carrito": cart.show_cart()
        elif page == "Historial": historial.show_history()
        elif page == "Soporte": soporte_adoptante.soporte_adoptante()
        