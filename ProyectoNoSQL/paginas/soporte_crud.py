import streamlit as st
import pandas as pd
from db import get_collection, to_dict

COL = get_collection("Soporte")

def soporte_crud():
    st.header("CRUD de Soporte 🆘")
    docs = list(COL.find())
    if docs:
        st.dataframe(pd.DataFrame([to_dict(d) for d in docs]), use_container_width=True)

    with st.expander("Enviar solicitud de soporte"):
        with st.form("form_add_sup"):            
            user = st.text_input("Usuario")
            asunto = st.text_input("Asunto")
            desc = st.text_area("Descripción")
            if st.form_submit_button("Enviar"):
                COL.insert_one({"user": user, "asunto": asunto, "descripcion": desc, "estatus": "Abierto"})
                st.success("Solicitud enviada.")
                st.rerun()

    ids = [str(d['_id']) for d in docs]
    if ids and st.button("Cerrar última solicitud"):
        COL.update_one({'_id': docs[-1]['_id']}, {'$set': {'estatus': 'Cerrado'}})
        st.success("Solicitud cerrada.")
        st.rerun()