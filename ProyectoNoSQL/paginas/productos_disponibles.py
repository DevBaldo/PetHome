import streamlit as st
from db import get_collection
from bson.objectid import ObjectId

def productos_disponibles():
    st.header("Productos Disponibles 🛒")
    PROD = get_collection("Productos")
    prods = list(PROD.find({"stock": {"$gt": 0}}))
    if not prods:
        st.info("No hay productos disponibles.")
        return
    for prod in prods:
        st.subheader(prod['nombre'])
        st.write(f"Precio: ${prod['precio']:.2f}")
        st.write(f"Stock: {prod['stock']}")
        qty = st.number_input("Cantidad", min_value=1, max_value=prod['stock'], key=str(prod['_id']))
        if st.button("Añadir al carrito", key="add_"+str(prod['_id'])):
            st.session_state.cart.append({
                '_id': prod['_id'], 'nombre': prod['nombre'],
                'precio': prod['precio'], 'cantidad': qty
            })
            st.success(f"{prod['nombre']} agregado al carrito.")
            st.rerun()