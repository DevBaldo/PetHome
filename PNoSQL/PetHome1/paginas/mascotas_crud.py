import streamlit as st
import pandas as pd
from bson import ObjectId
from db import get_collection, to_dict

COL_MASCOTAS = get_collection("Mascotas")
COL_REFUGIOS = get_collection("Refugios")

def mascotas_crud():
    st.header("CRUD de Mascotas 🐶🐱")
    
    # Obtener lista de refugios para el dropdown
    refugios = list(COL_REFUGIOS.find())
    opciones_refugios = {str(ref['_id']): ref['nombre'] for ref in refugios}
    
    # Listar mascotas con información de refugio
    docs = list(COL_MASCOTAS.find())
    
    if docs:
        # Convertir documentos a DataFrame con información de refugio
        data = []
        for d in docs:
            mascota = to_dict(d)
            mascota['edad'] = int(mascota.get('edad', 0))
            # Obtener nombre del refugio
            refugio_id = mascota.get('refugio_id')
            mascota['refugio'] = opciones_refugios.get(refugio_id, "Sin refugio") if refugio_id else "Sin refugio"
            data.append(mascota)
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)

    # Agregar nueva mascota
    with st.expander("Agregar Mascota"):
        with st.form("form_add_mascota", clear_on_submit=True):
            nombre = st.text_input("Nombre")
            especie = st.selectbox("Especie", ["Perro", "Gato", "Otro"])
            edad = st.number_input("Edad (años)", min_value=0, value=0)
            disp = st.checkbox("Disponible", value=True)

            imagen = st.file_uploader("Imagen de la mascota", type=['png','jpg','jpeg'])
            
            # Dropdown para seleccionar refugio
            if refugios:
                refugio_seleccionado = st.selectbox(
                    "Refugio",
                    options=list(opciones_refugios.keys()),
                    format_func=lambda x: opciones_refugios[x]
                )
            else:
                st.warning("No hay refugios registrados")
                refugio_seleccionado = None
            
            if st.form_submit_button("Guardar"):  
                mascota_data = {
                    "nombre": nombre, 
                    "especie": especie, 
                    "edad": int(edad),
                    "disponible": disp
                }
                if refugio_seleccionado:
                    mascota_data["refugio_id"] = refugio_seleccionado
                if imagen:
                    mascota_data["imagen"] = imagen.getvalue()
                    
                COL_MASCOTAS.insert_one(mascota_data)
                st.success("Mascota agregada exitosamente.")
                st.rerun()

    # Editar/Eliminar mascotas existentes
    if docs:
        ids = [str(d['_id']) for d in docs]
        sel = st.selectbox("Selecciona ID para editar/eliminar", ids)
        doc = COL_MASCOTAS.find_one({'_id': ObjectId(sel)})
    
    if doc:
        with st.form("form_edit_mascota"):
            nombre2 = st.text_input("Nombre", value=doc.get('nombre', ''))
            
            especies = ["Perro", "Gato", "Otro"]
            especie_actual = doc.get('especie', 'Perro')
            try:
                index_actual = especies.index(especie_actual)
            except ValueError:
                index_actual = 0
            
            especie2 = st.selectbox("Especie", especies, index=index_actual)
            edad2 = st.number_input("Edad", value=int(doc.get('edad', 0)), min_value=0)
            disp2 = st.checkbox("Disponible", value=doc.get('disponible', True))

            # Dropdown para editar refugio
            if refugios:
                refugio_actual = doc.get('refugio_id')
                index_refugio = list(opciones_refugios.keys()).index(refugio_actual) if refugio_actual in opciones_refugios else 0
                refugio_seleccionado = st.selectbox(
                    "Refugio",
                    options=list(opciones_refugios.keys()),
                    index=index_refugio,
                    format_func=lambda x: opciones_refugios[x]
                )
            else:
                st.warning("No hay refugios registrados")
                refugio_seleccionado = None

            #Subida de imagen opcional al editar
            nueva_imagen = st.file_uploader("Cambiar imagen (opcional)", type=['png', 'jpg', 'jpeg'])

            #Mostrar imagen actual
            if "imagen" in doc:
                st.image(doc["imagen"], caption="Imagen actual", width=300)

            # Botones de acción
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Actualizar"):
                    update_data = {
                        'nombre': nombre2, 
                        'especie': especie2, 
                        'edad': int(edad2),
                        'disponible': disp2
                    }
                    if refugio_seleccionado:
                        update_data['refugio_id'] = refugio_seleccionado
                    
                    #Si subió nueva imagen, se actualiza
                    if nueva_imagen:
                        update_data['imagen'] = nueva_imagen.getvalue()
                    
                    COL_MASCOTAS.update_one(
                        {'_id': doc['_id']}, 
                        {'$set': update_data}
                    )
                    st.success("Mascota actualizada.")
                    st.rerun()
            
            with col2:
                if st.form_submit_button("Eliminar"):
                    COL_MASCOTAS.delete_one({'_id': doc['_id']})
                    st.success("Mascota eliminada.")
                    st.rerun()