import streamlit as st
from db import get_collection
from bson.objectid import ObjectId
from datetime import date


def adoptar_page():
    st.header("Adoptar una Mascota 🏠🐾")
    
    # Obtener colecciones
    MASC = get_collection("Mascotas")
    REFUGIOS = get_collection("Refugios")
    ADOPCIONES = get_collection("Adopciones")
    
    # Obtener mascotas disponibles con información de refugio
    pets = list(MASC.find({"disponible": True}))
    refugios = {str(ref['_id']): ref for ref in REFUGIOS.find()}
    
    if not pets:
        st.info("No hay mascotas disponibles para adopción.")
        return
    
    # Mostrar cada mascota en cards
    cols = st.columns(2)  # 2 columnas para mejor organización
    for i, pet in enumerate(pets):
        with cols[i % 2]:  # Alternar entre columnas
            with st.container(border=True):
                # Header con nombre y especie
                st.subheader(f"{pet['nombre']} ({pet['especie']})")
                
                # Información básica
                st.write(f"🐾 **Edad:** {pet.get('edad', 'Desconocida')} años")
                
                # Mostrar información del refugio si existe
                if 'refugio_id' in pet and pet['refugio_id'] in refugios:
                    refugio = refugios[pet['refugio_id']]
                    st.write(f"🏠 **Refugio:** {refugio.get('nombre', 'Desconocido')}")
                    st.write(f"📍 **Ubicación:** {refugio.get('ubicacion', 'No especificada')}")
                else:
                    st.write("🏠 **Refugio:** No asignado")
                
                
                if "imagen" in pet:
                    st.image(pet["imagen"], use_container_width=True)
                else:
                    st.image("https://placehold.co/400x200?text=Foto+de+" + pet['nombre'], 
                             use_container_width=True)
                
                # Botón de adopción
                if st.button(f"Adoptar {pet['nombre']}", key=str(pet['_id'])):
                    get_collection("Adopciones").insert_one({
                        "user": st.session_state.user['username'],
                        "mascota": pet['nombre'],
                        "fecha": date.today().isoformat()
                    })
                    MASC.update_one({"_id": ObjectId(pet['_id'])}, {"$set": {"disponible": False}})
                    st.success(f"¡Has adoptado a {pet['nombre']}!")
                    st.rerun()
                
                # Espaciado entre mascotas
                st.write("---")