import streamlit as st
import pandas as pd
from db import get_collection, to_dict
from bson.objectid import ObjectId


def show_history():
    st.header("Tu Historial 📜")
    tabs = st.tabs(["Adopciones", "Compras"])
    with tabs[0]:
        adop = list(get_collection("Adopciones").find({"user": st.session_state.user['username']}))
        if adop:
            df = pd.DataFrame([to_dict(d) for d in adop])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No tienes adopciones registradas.")
    with tabs[1]:
        comp = list(get_collection("Compras").find({"user": st.session_state.user['username']}))
        if comp:
            rows = []
            for c in comp:
                for itm in c['items']:
                    rows.append({
                        "fecha": c['fecha'],
                        "producto": itm['nombre'],
                        "cantidad": itm['cantidad'],
                        "subtotal": itm['precio'] * itm['cantidad']
                    })
            df2 = pd.DataFrame(rows)
            st.dataframe(df2, use_container_width=True)
        else:
            st.info("No tienes compras registradas.")