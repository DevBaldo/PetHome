import streamlit as st
import pandas as pd
from bson import ObjectId  # <-- Add this import
from db import get_collection, to_dict

def productos_crud():
    st.header("CRUD de Productos 🛍️")
    COL = get_collection("Productos")
    docs = list(COL.find())
    
    if docs:
        st.dataframe(pd.DataFrame([to_dict(d) for d in docs]), use_container_width=True)

    with st.expander("Agregar Producto"):
        with st.form("form_add_prod", clear_on_submit=True):
            nombre = st.text_input("Nombre")
            precio = st.number_input("Precio", min_value=0.0, format="%.2f")
            stock = st.number_input("Stock", min_value=0)
            if st.form_submit_button("Guardar"):
                COL.insert_one({"nombre": nombre, "precio": precio, "stock": stock})
                st.success("Producto agregado.")
                st.rerun()

    # Editar/Eliminar
    ids = [str(d['_id']) for d in docs]
    if ids:
        sel = st.selectbox("ID producto", ids)
        doc = COL.find_one({'_id': ObjectId(sel)})  # <-- Fixed line
        
        if doc:
            with st.form("form_edit_prod"):
                nombre2 = st.text_input("Nombre", value=doc['nombre'])
                precio2 = st.number_input("Precio", value=doc['precio'], format="%.2f")
                stock2 = st.number_input("Stock", value=doc['stock'], min_value=0)
                c1, c2 = st.columns(2)
                with c1:
                    if st.form_submit_button("Actualizar"):
                        COL.update_one(
                            {'_id': ObjectId(sel)},
                            {'$set': {'nombre': nombre2, 'precio': precio2, 'stock': stock2}}
                        )
                        st.success("Producto actualizado.")
                        st.rerun()
                with c2:
                    if st.form_submit_button("Eliminar"):
                        COL.delete_one({'_id': ObjectId(sel)})
                        st.success("Producto eliminado.")
                        st.rerun()