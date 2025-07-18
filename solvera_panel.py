
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
datos = pd.read_csv("solvera_datos_simulados.csv", parse_dates=["FechaHora"])
sugerencias = pd.read_csv("solvera_sugerencias.csv", parse_dates=["Fecha"])

# Título y nombre del proyecto
st.set_page_config(page_title="Solvera - Panel Solar Inteligente", layout="wide")
st.title("☀️ SOLVERA - Panel Solar Inteligente")

# Fecha seleccionada
fecha_seleccionada = st.date_input("Seleccioná un día para analizar", value=datos["FechaHora"].dt.date.max())
datos_dia = datos[datos["FechaHora"].dt.date == fecha_seleccionada]

# Resumen diario
st.subheader("🔎 Resumen del día")
prod_total = datos_dia["ProduccionSolar_kWh"].sum()
cons_total = datos_dia["Consumo_kWh"].sum()
ahorro_estimado = round(prod_total * 200, 2)  # suposición: 200 ARS por kWh

col1, col2, col3 = st.columns(3)
col1.metric("Producción Solar (kWh)", f"{prod_total:.2f}")
col2.metric("Consumo Total (kWh)", f"{cons_total:.2f}")
col3.metric("Ahorro Estimado", f"${ahorro_estimado:.2f} ARS")

# Gráfico comparativo
st.subheader("📊 Producción vs Consumo por hora")
fig, ax = plt.subplots()
ax.plot(datos_dia["FechaHora"].dt.hour, datos_dia["ProduccionSolar_kWh"], label="Producción Solar", color="orange")
ax.plot(datos_dia["FechaHora"].dt.hour, datos_dia["Consumo_kWh"], label="Consumo", color="blue")
ax.set_xlabel("Hora del día")
ax.set_ylabel("kWh")
ax.legend()
st.pyplot(fig)

# Sugerencia IA
st.subheader("🤖 Sugerencia Inteligente del Día")
sug = sugerencias[sugerencias["Fecha"] == pd.to_datetime(fecha_seleccionada)].squeeze()
if not sug.empty:
    st.success(sug["SugerenciaIA"])
else:
    st.info("No hay sugerencia disponible para este día.")
