
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import locale

# Intentar configurar locale español para parsing fechas en español
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Linux/Mac
except:
    try:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')  # Windows
    except:
        pass

@st.cache_data
def cargar_datos():
    datos = pd.read_csv("solvera_datos_simulados.csv", parse_dates=["FechaHora"])

    # Corregir coma decimal a punto decimal en columnas numéricas
    cols_num = ["Producción Solar_kWh", "Consumo_kWh", "RadiaciónSolar_Wm2", "Temperatura_C"]
    for col in cols_num:
        datos[col] = datos[col].astype(str).str.replace(',', '.').astype(float)
    
    datos["FechaHora"] = pd.to_datetime(datos["FechaHora"], dayfirst=True)
    return datos

@st.cache_data
def cargar_sugerencias():
    sugerencias = pd.read_csv("solvera_sugerencias.csv")
    # Convertir fechas literales en español a datetime
    sugerencias["Fecha"] = pd.to_datetime(sugerencias["Fecha"], format="%d de %B de %Y")
    return sugerencias

datos = cargar_datos()
sugerencias = cargar_sugerencias()

st.set_page_config(page_title="Solvera - Panel Solar Inteligente", layout="wide")
st.title("☀️ SOLVERA - Panel Solar Inteligente")

fecha_seleccionada = st.date_input("Seleccioná un día para analizar", value=datos["FechaHora"].dt.date.max())
datos_dia = datos[datos["FechaHora"].dt.date == fecha_seleccionada]

st.subheader("🔎 Resumen del día")
prod_total = datos_dia["Producción Solar_kWh"].sum()
cons_total = datos_dia["Consumo_kWh"].sum()
ahorro_estimado = round(prod_total * 200, 2)

col1, col2, col3 = st.columns(3)
col1.metric("Producción Solar (kWh)", f"{prod_total:.2f}")
col2.metric("Consumo Total (kWh)", f"{cons_total:.2f}")
col3.metric("Ahorro Estimado", f"${ahorro_estimado:.2f} ARS")

st.subheader("📊 Producción vs Consumo por hora")
fig, ax = plt.subplots()
ax.plot(datos_dia["FechaHora"].dt.hour, datos_dia["Producción Solar_kWh"], label="Producción Solar", color="orange")
ax.plot(datos_dia["FechaHora"].dt.hour, datos_dia["Consumo_kWh"], label="Consumo", color="blue")
ax.set_xlabel("Hora del día")
ax.set_ylabel("kWh")
ax.legend()
st.pyplot(fig)

st.subheader("🤖 Sugerencia Inteligente del Día")
sug = sugerencias[sugerencias["Fecha"] == pd.to_datetime(fecha_seleccionada)].squeeze()
if not sug.empty:
    st.success(sug["SugerenciaIA"])
else:
    st.info("No hay sugerencia disponible para este día.")
