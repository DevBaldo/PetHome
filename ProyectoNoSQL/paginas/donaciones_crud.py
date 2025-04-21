import streamlit as st
import pandas as pd
from db import get_collection, to_dict

COL = get_collection("Donaciones")


def donaciones_crud():
    st.header("CRUD de Donaciones 🙏")
    docs = list(COL.find())
    if docs:
        st.dataframe(pd.DataFrame([to_dict(d) for d in docs]), use_container_width=True)

    with st.expander("Registrar Donación"):
        with st.form("form_add_don"):            
            nombre = st.text_input("Donante")
            monto = st.number_input("Monto", min_value=0.0, format="%.2f")
            fecha = st.date_input("Fecha")
            if st.form_submit_button("Guardar"):
                COL.insert_one({"user": nombre, "monto": monto, "fecha": fecha.isoformat()})
                st.success("Donación registrada.")
                st.rerun()

    ids = [str(d['_id']) for d in docs]
    if ids and st.button("Eliminar última donación"):
        COL.delete_one({'_id': docs[-1]['_id']})
        st.success("Última donación eliminada.")
        st.rerun()