import streamlit as st
import pandas as pd
from db import get_collection, to_dict

COL = get_collection("Cuidados")

def cuidados_crud():
    st.header("CRUD de Cuidados 🏥")
    docs = list(COL.find())
    if docs:
        st.dataframe(pd.DataFrame([to_dict(d) for d in docs]), use_container_width=True)

    with st.expander("Agregar Cuidado"):
        with st.form("form_add_cui"):            
            titulo = st.text_input("Título")
            desc = st.text_area("Descripción")
            if st.form_submit_button("Guardar"):
                COL.insert_one({"titulo": titulo, "descripcion": desc})
                st.success("Cuidado agregado.")
                st.rerun()

    ids = [str(d['_id']) for d in docs]
    if ids and st.button("Eliminar último cuidado"):
        COL.delete_one({'_id': docs[-1]['_id']})
        st.success("Último cuidado eliminado.")
        st.rerun()