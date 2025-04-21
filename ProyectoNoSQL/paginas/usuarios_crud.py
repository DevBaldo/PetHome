import streamlit as st
import pandas as pd
from db import get_collection, to_dict
from werkzeug.security import generate_password_hash

COL = get_collection("Usuarios")

def usuarios_crud():
    st.header("CRUD de Usuarios ⚙️")
    docs = list(COL.find())
    if docs:
        st.dataframe(pd.DataFrame([to_dict(d) for d in docs]), use_container_width=True)

    with st.expander("Agregar Usuario"):
        with st.form("form_add_usr"):            
            user = st.text_input("Usuario")
            pwd = st.text_input("Contraseña", type="password")
            role = st.selectbox("Rol", ["admin", "adoptante"])
            if st.form_submit_button("Guardar"):
                hashed = generate_password_hash(pwd)
                COL.insert_one({"username": user, "password": hashed, "role": role})
                st.success("Usuario agregado.")
                st.rerun()

    ids = [str(d['_id']) for d in docs]
    if ids and st.button("Eliminar último usuario"):
        COL.delete_one({'_id': docs[-1]['_id']})
        st.success("Último usuario eliminado.")
        st.rerun()