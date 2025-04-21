import streamlit as st
import pandas as pd
from bson import ObjectId  
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
            imagen = st.file_uploader("Imagen del producto", type=['png', 'jpg', 'jpeg'])  #imagen nueva
            
            if st.form_submit_button("Guardar"):
                producto_data = {"nombre": nombre, "precio": precio, "stock": stock}
                if imagen:
                    producto_data["imagen"] = imagen.getvalue()  
                COL.insert_one(producto_data)
                st.success("Producto agregado.")
                st.rerun()

    # Editar/Eliminar
    ids = [str(d['_id']) for d in docs]
    if ids:
        sel = st.selectbox("ID producto", ids)
        doc = COL.find_one({'_id': ObjectId(sel)})  
        
        if doc:
            with st.form("form_edit_prod"):
                nombre2 = st.text_input("Nombre", value=doc['nombre'])
                precio2 = st.number_input("Precio", value=doc['precio'], format="%.2f")
                stock2 = st.number_input("Stock", value=doc['stock'], min_value=0)

                #Mostrar imagen actual si existe
                if "imagen" in doc:
                    st.image(doc["imagen"], caption="Imagen actual", width=200)
                
                imagen_nueva = st.file_uploader("Nueva imagen (opcional)", type=['png', 'jpg', 'jpeg'])  # nueva imagen

                c1, c2 = st.columns(2)
                with c1:
                    if st.form_submit_button("Actualizar"):
                        update_data = {
                            'nombre': nombre2,
                            'precio': precio2,
                            'stock': stock2
                        }
                        if imagen_nueva:
                            update_data['imagen'] = imagen_nueva.getvalue()
                        COL.update_one({'_id': ObjectId(sel)}, {'$set': update_data})
                        st.success("Producto actualizado.")
                        st.rerun()
                with c2:
                    if st.form_submit_button("Eliminar"):
                        COL.delete_one({'_id': ObjectId(sel)})
                        st.success("Producto eliminado.")
                        st.rerun()