import streamlit as st
from db import get_collection
from datetime import datetime


def donaciones_adoptante():
    st.header("Realizar Donación 🙏")
    with st.form("don_form"):
        monto = st.number_input("Monto a donar", min_value=1.0, format="%.2f")
        if st.form_submit_button("Donar"):
            get_collection("Donaciones").insert_one({
                "user": st.session_state.user['username'],
                "monto": monto,
                "fecha": datetime.now().isoformat()
            })
            st.success("¡Gracias por tu donación!")