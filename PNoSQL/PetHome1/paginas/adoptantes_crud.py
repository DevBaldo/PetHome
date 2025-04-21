import streamlit as st
import pandas as pd
from bson import ObjectId
from db import get_collection, to_dict
from werkzeug.security import generate_password_hash

COL = get_collection("Usuarios")

def adoptantes_crud():
    st.header("CRUD de Adoptantes 👤")
    docs = list(COL.find({"role": "adoptante"}))
    if docs:
        st.dataframe(pd.DataFrame([to_dict(d) for d in docs]), use_container_width=True)

    with st.expander("Agregar Adoptante"):
        with st.form("form_add_adopt"):            
            user = st.text_input("Usuario")
            pwd = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Guardar"):
                hashed = generate_password_hash(pwd)
                COL.insert_one({"username": user, "password": hashed, "role": "adoptante"})
                st.success("Adoptante creado.")
                st.rerun()

    ids = [str(d['_id']) for d in docs]
    if ids:
        sel = st.selectbox("ID adoptante", ids)
        doc = COL.find_one({'_id': ObjectId(sel)})
        if doc:
            if st.button("Eliminar Adoptante"):
                COL.delete_one({'_id': doc['_id']})
                st.success("Adoptante eliminado.")
                st.rerun()