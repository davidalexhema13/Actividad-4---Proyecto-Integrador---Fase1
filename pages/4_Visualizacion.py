import streamlit as st
import pandas as pd
import altair as alt
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utilidades import cargar_datos, pipeline_validacion

st.set_page_config(page_title="Dashboard Analítico", page_icon="📈", layout="wide")

st.title("📈 Dashboard Analítico: Presuntos Suicidios en Colombia")

# --- 1. CARGA DE DATOS CENTRALIZADA ---
# Se simplifica el flujo priorizando los datos del Módulo 3. Si no existen, carga el general.
@st.cache_data(show_spinner=False)
def cargar_fuente_fallback():
    return pipeline_validacion(cargar_datos())

if "df_filtrado" in st.session_state and st.session_state["df_filtrado"] is not None:
    df_act = st.session_state["df_filtrado"]
    st.sidebar.success("✅ Mostrando datos filtrados desde Módulo 3.")
else:
    df_act = cargar_fuente_fallback()
    st.sidebar.info("💡 Mostrando base de datos global. Ve al Módulo 3 si deseas aplicar filtros.")

if df_act is None or df_act.empty:
    st.error("📉 El conjunto de datos está vacío. Ajusta los filtros en el Módulo 3.")
    st.stop()

# --- 2. AYUDANTES DE SÍNTESIS ---
def calcular_top(df, col):
    """Devuelve la categoría más frecuente y su porcentaje."""
    if col not in df.columns: return "N/A", 0
    serie = df[col].dropna()
    if serie.empty: return "N/A", 0
    top = serie.mode().iloc[0]
    perc = (serie.value_counts().iloc[0] / len(serie)) * 100
    return top, perc

# --- 3. KPIs DIRECTOS ---
top_depto, perc_depto = calcular_top(df_act, "Departamento del hecho DANE")
top_meca, perc_meca = calcular_top(df_act, "Mecanismo Causal de la Lesión Fatal")

k1, k2, k3 = st.columns(3)
k1.metric("📄 Total de Registros", f"{df_act.shape[0]:,}")
k2.metric("📌 Departamento Más Afectado", top_depto, f"{perc_depto:.1f}% de concentración")
k3.metric("⚠️ Mecanismo Principal", top_meca, f"{perc_meca:.1f}% del total")

st.divider()

# --- 4. SECCIONES DE VISUALIZACIÓN ---
colA, colB = st.columns(2)

# TENDENCIAS 
with colA:
    st.subheader("Evolución Histórica")
    col_x = "Año del hecho"
    if col_x in df_act.columns:
        # Se remueven selectores innecesarios. Muestra la tendencia neta directamente.
        df_tend = df_act.groupby(col_x).size().reset_index(name="Casos")
        chart_linea = alt.Chart(df_tend).mark_line(point=True, color="#2c3e50").encode(
            x=alt.X(f"{col_x}:O", title="Año"),
            y=alt.Y("Casos:Q"),
            tooltip=[col_x, "Casos"]
        ).properties(height=320)
        st.altair_chart(chart_linea, use_container_width=True)
        
        # Insight
        if len(df_tend) >= 2:
            var = df_tend.iloc[-1]["Casos"] - df_tend.iloc[0]["Casos"]
            tend = "al alza" if var > 0 else "a la baja" if var < 0 else "estable"
            st.caption(f"💡 *Tendencia general **{tend}** comparando el primer y último periodo visible (*{df_tend.iloc[0][col_x]} - {df_tend.iloc[-1][col_x]}*).*")

# DISTRIBUCIÓN
with colB:
    st.subheader("Distribución por Sexo")
    col_sex = "Sexo de la victima"
    if col_sex in df_act.columns:
        df_pie = df_act.groupby(col_sex).size().reset_index(name="Total")
        chart_pie = alt.Chart(df_pie).mark_arc(innerRadius=50).encode(
            theta=alt.Theta("Total:Q", stack=True),
            color=alt.Color(f"{col_sex}:N", scale=alt.Scale(scheme='tableau10'), title=""),
            tooltip=[col_sex, "Total"]
        ).properties(height=320)
        st.altair_chart(chart_pie, use_container_width=True)

st.divider()

# COMPARACIONES
st.subheader("Principales Focos de Incidencia (Departamentos)")
col_dpto = "Departamento del hecho DANE"
if col_dpto in df_act.columns:
    df_bar = df_act.groupby(col_dpto).size().reset_index(name="Casos").sort_values("Casos", ascending=False).head(10)
    chart_bar = alt.Chart(df_bar).mark_bar().encode(
        x=alt.X('Casos:Q'),
        y=alt.Y(f'{col_dpto}:N', sort='-x', title=""),
        color=alt.value('#3498db'),
        tooltip=[col_dpto, 'Casos']
    ).properties(height=350)
    st.altair_chart(chart_bar, use_container_width=True)

st.divider()

# --- 5. EXPORTACIÓN LIMPIA ---
st.download_button(
    label="🔽 Exportar Conjunto de Datos Actual (CSV)",
    data=df_act.to_csv(index=False).encode('utf-8'),
    file_name="analisis_suicidios_filtrado.csv",
    mime="text/csv",
    use_container_width=True
)