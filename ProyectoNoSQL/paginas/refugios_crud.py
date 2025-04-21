import streamlit as st
import pandas as pd
from bson import ObjectId
from db import get_collection, to_dict

COL_MASCOTAS = get_collection("Mascotas")
COL_REFUGIOS = get_collection("Refugios")

def refugios_crud():
    st.header("CRUD de Refugios 🏠")
    docs = list(COL_REFUGIOS.find())
    if docs:
        st.dataframe(pd.DataFrame([to_dict(d) for d in docs]), use_container_width=True)

    with st.expander("Agregar Refugio"):
        with st.form("form_add_ref"):            
            nombre = st.text_input("Nombre del refugio")
            ubic = st.text_input("Ubicación")
            if st.form_submit_button("Guardar"):
                COL_REFUGIOS.insert_one({"nombre": nombre, "ubicacion": ubic})
                st.success("Refugio agregado.")
                st.rerun()

    ids = [str(d['_id']) for d in docs]
    if ids:
        sel = st.selectbox("ID refugio", ids)
        doc = COL_REFUGIOS.find_one({'_id': ObjectId(sel)})
        if doc:
            col1, col2 = st.columns(2)
            with col1:
                with st.form("form_edit_ref"):
                    nombre2 = st.text_input("Nombre", value=doc.get('nombre', ''))
                    ubic2 = st.text_input("Ubicación", value=doc.get('ubicacion', ''))
                    if st.form_submit_button("Actualizar"):
                        COL_REFUGIOS.update_one(
                            {'_id': doc['_id']}, 
                            {'$set': {
                                'nombre': nombre2, 
                                'ubicacion': ubic2
                            }}
                        )
                        st.success("Refugio actualizado.")
                        st.rerun()
            with col2:
                if st.button("Eliminar Refugio"):
                    # Verificar si hay mascotas asociadas antes de eliminar
                    mascotas_asociadas = COL_MASCOTAS.count_documents({'refugio_id': str(doc['_id'])})
                    if mascotas_asociadas > 0:
                        st.error(f"No se puede eliminar: hay {mascotas_asociadas} mascotas asociadas a este refugio")
                    else:
                        COL_REFUGIOS.delete_one({'_id': doc['_id']})
                        st.success("Refugio eliminado.")
                        st.rerun()