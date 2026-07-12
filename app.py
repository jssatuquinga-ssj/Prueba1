import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Salve Faccha - Resultados", layout="wide")

# Ruta del archivo Excel
archivo = "Resumen_General_Modelo_Mejorado_8Subcuencas.xlsx"
# Verificar existencia
if not os.path.exists(archivo):
    st.error("No se encontró el archivo Excel:")
    st.write(archivo)
    st.stop()

st.title("Modelo Hidrológico - Embalse Salve Faccha")
st.subheader("Visualización de resultados del modelo mejorado de 8 subcuencas BHSF")

# Leer hojas Excel
try:
    resumen = pd.read_excel(archivo, sheet_name="Resumen_Subcuencas")
    caudales = pd.read_excel(archivo, sheet_name="Caudales_Horarios")
    sistema = pd.read_excel(archivo, sheet_name="Resumen_Sistema")

except Exception as e:
    st.error("Error leyendo el archivo Excel")
    st.write(e)
    st.stop()


sub = st.selectbox(
    "Seleccione subcuenca",
    resumen["Subcuenca"].unique()
)

fila = resumen[resumen["Subcuenca"] == sub].iloc[0]


c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Caudal medio (m³/s)",
    round(fila["Q_medio_m3s"], 3)
)

c2.metric(
    "Caudal máximo (m³/s)",
    round(fila["Q_max_m3s"], 3)
)

c3.metric(
    "Volumen (m³)",
    f'{fila["Volumen_total_m3"]:,.0f}'
)

c4.metric(
    "NSE",
    round(fila["NSE"], 3)
)


st.subheader("Hidrograma horario")

col = "Q_" + sub + "_m3s"

if col in caudales.columns:

    graf = caudales[["Fecha", col]].copy()
    graf = graf.set_index("Fecha")

    st.line_chart(graf)

else:
    st.warning(f"No existe la columna {col} en Caudales_Horarios")


st.subheader("Resumen de subcuencas")
st.dataframe(resumen)


st.subheader("Resultados del sistema completo")
st.dataframe(sistema)



st.download_button(
    "Descargar resultados",
    resumen.to_csv(index=False),
    "resumen_subcuencas.csv"
)

