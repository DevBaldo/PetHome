from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import streamlit as st

try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client.PetHome
except ConnectionFailure:
    st.error("No se pudo conectar a MongoDB. Revisa tu URI en .streamlit/secrets.toml.")


def get_collection(name: str):
    """Retorna la colección de Mongo correspondiente."""
    return db[name]


def to_dict(doc: dict) -> dict:
    """Convierte ObjectId a string para visualización."""
    doc = {**doc}
    doc["_id"] = str(doc.get("_id"))
    return doc