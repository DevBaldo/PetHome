import streamlit as st
import pandas as pd
from db import get_collection, to_dict
from bson import ObjectId

COL = get_collection("Adopciones")
USERS = get_collection("Usuarios")
MASC = get_collection("Mascotas")


def adopciones_crud():
    st.header("CRUD de Adopciones 🏠")
    docs = list(COL.find())
    if docs:
        df = pd.DataFrame([to_dict(d) for d in docs])
        st.dataframe(df, use_container_width=True)

    with st.expander("Registrar Adopción"):
        with st.form("form_add_adop"):            
            user_opts = [u['username'] for u in USERS.find({"role": "adoptante"})]
            masc_opts = [m['nombre'] for m in MASC.find({"disponible": True})]
            user_sel = st.selectbox("Adoptante", user_opts)
            masc_sel = st.selectbox("Mascota", masc_opts)
            fecha = st.date_input("Fecha de adopción")
            if st.form_submit_button("Registrar"):
                COL.insert_one({"user": user_sel, "mascota": masc_sel, "fecha": fecha.isoformat()})
                # marcar mascota no disponible
                MASC.update_one({"nombre": masc_sel}, {"$set": {"disponible": False}})
                st.success("Adopción registrada.")
                st.rerun()

    # Editar/Eliminar
    ids = [str(d['_id']) for d in docs]
    if ids:
        sel = st.selectbox("ID adopción", ids)
        doc = COL.find_one({'_id': ObjectId(sel)})
        if doc:
            with st.form("form_edit_adop"):
                fecha2 = st.date_input("Fecha", value=pd.to_datetime(doc['fecha']))
                c1, c2 = st.columns(2)
                with c1:
                    if st.form_submit_button("Actualizar"):
                        COL.update_one({'_id': ObjectId(sel)}, {'$set': {'fecha': fecha2.isoformat()}})
                        st.success("Adopción actualizada.")
                        st.rerun()
                with c2:
                    if st.form_submit_button("Eliminar"):
                        COL.delete_one({'_id': ObjectId(sel)})
                        st.success("Adopción eliminada.")
                        st.rerun()