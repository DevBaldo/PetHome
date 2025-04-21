import streamlit as st
import pandas as pd
from db import get_collection, to_dict

COL = get_collection("Comentarios")

def comentarios_crud():
    st.header("CRUD de Comentarios 💬")
    docs = list(COL.find())
    if docs:
        st.dataframe(pd.DataFrame([to_dict(d) for d in docs]), use_container_width=True)

    with st.expander("Agregar Comentario"):
        with st.form("form_add_com"):            
            user = st.text_input("Usuario")
            texto = st.text_area("Comentario")
            if st.form_submit_button("Guardar"):
                COL.insert_one({"user": user, "texto": texto})
                st.success("Comentario agregado.")
                st.rerun()

    ids = [str(d['_id']) for d in docs]
    if ids and st.button("Eliminar último comentario"):
        COL.delete_one({'_id': docs[-1]['_id']})
        st.success("Último comentario eliminado.")
        st.rerun()