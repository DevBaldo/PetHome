import streamlit as st
from db import get_collection
from datetime import date
from bson.objectid import ObjectId


def show_cart():
    st.header("Tu Carrito 🛒")
    cart = st.session_state.get("cart", [])
    if not cart:
        st.info("Tu carrito está vacío.")
        return
    total = sum(item['precio'] * item['cantidad'] for item in cart)
    for i, item in enumerate(cart):
        st.write(f"{item['nombre']} - ${item['precio']:.2f} x {item['cantidad']}")
        if st.button("Eliminar", key=f"del_{i}"):
            cart.pop(i)
            st.rerun()
    st.subheader(f"Total: ${total:.2f}")
    if st.button("Pagar Ahora"):
        COMP = get_collection("Compras")
        COMP.insert_one({
            "user": st.session_state.user['username'],
            "items": cart,
            "total": total,
            "fecha": date.today().isoformat()
        })
        PROD = get_collection("Productos")
        for item in cart:
            PROD.update_one({"_id": ObjectId(item['_id'])}, {"$inc": {"stock": -item['cantidad']}})
        st.session_state.cart = []
        st.success("Compra realizada con éxito.")
        st.rerun()