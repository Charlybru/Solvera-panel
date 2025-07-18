import streamlit as st
import pandas as pd

st.title("Prueba de carga CSV alternativa")

try:
    datos = pd.read_csv("solvera_datos_simulados.csv")
    st.write("Datos simulados cargados:")
    st.dataframe(datos.head())
except Exception as e:
    st.error(f"Error al cargar datos simulados: {e}")

try:
    sugerencias = pd.read_csv("solvera_sugerencias.csv")
    st.write("Sugerencias cargadas:")
    st.dataframe(sugerencias.head())
except Exception as e:
    st.error(f"Error al cargar sugerencias: {e}")
