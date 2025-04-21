import streamlit as st
from db import get_collection
from werkzeug.security import generate_password_hash, check_password_hash

USERS = get_collection("Usuarios")


def register_user(username: str, password: str, role: str = "adoptante") -> tuple[bool, str]:
    """Registra un nuevo usuario con rol 'adoptante' o 'admin'."""
    if USERS.find_one({"username": username}):
        return False, "Usuario ya existe"
    hashed = generate_password_hash(password)
    USERS.insert_one({"username": username, "password": hashed, "role": role})
    return True, "Usuario registrado correctamente"


def login_user(username: str, password: str) -> bool:
    """Valida credenciales y guarda sesión."""
    user = USERS.find_one({"username": username})
    if user and check_password_hash(user["password"], password):
        st.session_state.user = {"username": user["username"], "role": user["role"]}
        
        if "cart" not in st.session_state:
            st.session_state.cart = []
        return True
    return False