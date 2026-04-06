import streamlit as st
import pandas as pd
import altair as alt
import sys
import os

# Ajuste para importar la capa abstracta desde la raíz
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utilidades import cargar_datos, pipeline_validacion, aplicar_filtros_puros

st.set_page_config(page_title="Filtros y Limpieza", page_icon="⚙️", layout="wide")

st.title("⚙️ Módulo 3: Interfaz de Filtros y Consolidación de Datos")
st.markdown("""
Configura un entorno de búsqueda granular. Ajusta los filtros y presiona **Aplicar Filtros** para ver los cambios reflejados en el dashboard. El sistema se encarga internamente de normalizar y pulir las entradas (pipeline de validación).
""")

# 🔄 BOTÓN PARA FORZAR RECARGA
if st.button("🔄 Recargar datos (forzar pipeline)"):
    st.session_state.pop("df_raw", None)
    st.session_state.pop("filtros_aplicados", None)
    st.rerun()

# 🔥 CARGA CON PIPELINE
with st.spinner("Cargando y validando Pipeline base..."):
    try:
        df = cargar_datos()
        df_validado = pipeline_validacion(df)
        st.session_state.df_raw = df_validado
    except Exception as e:
        st.error(f"💥 ERROR REAL EN PIPELINE: {e}")
        st.stop()

df_clean = st.session_state.df_raw

if df_clean is None or df_clean.empty:
    st.error("🚫 Ocurrió un error en el origen de los datos o el pipeline destruyó el contenido (posible csv corrupto).")
    st.stop()

st.info(f"💾 Se ha cargado el modelo base pre-validado con **{df_clean.shape[0]}** registros íntegros.")

# -----------------------------
# CONSTRUCCIÓN DE FILTROS
# -----------------------------
st.subheader("Arquitectura de Filtros")

col1, col2, col3 = st.columns(3)

# COL 1: Espacio-Temporal
with col1:
    st.markdown("#### ⏳ Dimensión Espacio-Temporal")

    min_y = int(df_clean["Año del hecho"].min())
    max_y = int(df_clean["Año del hecho"].max())
    rango_anos = st.slider("Rango de Años:", min_y, max_y, (min_y, max_y))

    if "Mes del hecho" in df_clean.columns:
        meses_uni = df_clean["Mes del hecho"].dropna().unique().tolist()
        sel_meses = st.multiselect("Meses de Registro:", meses_uni, default=[])
    else:
        sel_meses = []

    if "Dia del hecho" in df_clean.columns:
        dias_uni = df_clean["Dia del hecho"].dropna().unique().tolist()
        sel_dias = st.multiselect("Día de la Semana:", dias_uni, default=[])
    else:
        sel_dias = []

# COL 2: Geografía Relacional
with col2:
    st.markdown("#### 🗺️ Dimensión Geográfica")

    if "Departamento del hecho DANE" in df_clean.columns:
        deptos_uni = sorted(df_clean["Departamento del hecho DANE"].dropna().unique().tolist())
        opciones_dpt = ["(Todos)"] + deptos_uni
        sel_depto = st.selectbox("Seleccione Departamento:", opciones_dpt)

        sel_muni = []
        if sel_depto != "(Todos)" and "Municipio del hecho DANE" in df_clean.columns:
            muni_filtrados = df_clean[df_clean["Departamento del hecho DANE"] == sel_depto]
            muni_uni = sorted(muni_filtrados["Municipio del hecho DANE"].dropna().unique().tolist())
            sel_muni = st.multiselect("Municipios (relacionado):", muni_uni, default=[])
    else:
        sel_depto = "(Todos)"
        sel_muni = []

# COL 3: Contexto / Demografía
with col3:
    st.markdown("#### 👥 Dimensión Causal / Demográfica")

    if "Sexo de la victima" in df_clean.columns:
        sex_uni = sorted(df_clean["Sexo de la victima"].dropna().unique().tolist())
        sel_sexo = st.multiselect("Género/Sexo:", sex_uni, default=sex_uni)
    else:
        sex_uni = []
        sel_sexo = []

    if "Grupo de Edad Quinquenal " in df_clean.columns:
        edad_uni = sorted(df_clean["Grupo de Edad Quinquenal "].dropna().unique().tolist())
        sel_edad = st.multiselect("Grupo Etario:", edad_uni, default=[])
    else:
        sel_edad = []

    if "Mecanismo Causal de la Lesión Fatal" in df_clean.columns:
        mec_uni = sorted(df_clean["Mecanismo Causal de la Lesión Fatal"].dropna().unique().tolist())
        sel_mec = st.multiselect("Mecanismo Causal:", mec_uni, default=[])
    else:
        sel_mec = []

# --- FILTROS SOCIOCULTURALES ---
st.markdown("#### 🔍 Dimensión Sociocultural")
col4, col5, col6 = st.columns(3)

with col4:
    if "Estado Civil" in df_clean.columns:
        ec_uni = sorted(df_clean["Estado Civil"].dropna().unique().tolist())
        sel_estado_civil = st.multiselect("Estado Civil:", ec_uni, default=[])
    else:
        sel_estado_civil = []

with col5:
    if "Escolaridad" in df_clean.columns:
        esc_uni = sorted(df_clean["Escolaridad"].dropna().unique().tolist())
        sel_escolaridad = st.multiselect("Escolaridad:", esc_uni, default=[])
    else:
        sel_escolaridad = []

with col6:
    if "Ancestro Racial" in df_clean.columns:
        anc_uni = sorted(df_clean["Ancestro Racial"].dropna().unique().tolist())
        sel_ancestro = st.multiselect("Ancestro Racial:", anc_uni, default=[])
    else:
        sel_ancestro = []

st.divider()

# Botones de acción
btn_col1, btn_col2 = st.columns([1, 5])
with btn_col1:
    aplicar = st.button("✅ Aplicar Filtros", type="primary", use_container_width=True)
with btn_col2:
    if st.button("🗑️ Limpiar Filtros", use_container_width=True):
        st.session_state.pop("filtros_aplicados", None)
        st.rerun()

# -----------------------------
# LÓGICA DE FILTROS CON ESTADO
# -----------------------------
if "filtros_aplicados" not in st.session_state:
    st.session_state.filtros_aplicados = {
        "rango_anios": (min_y, max_y),
        "meses": [], "dias": [],
        "departamento": None, "municipios": [],
        "sexos": sex_uni,
        "grupos_edad": [], "mecanismos": [],
        "estado_civil": [], "escolaridad": [], "ancestro_racial": []
    }

if aplicar:
    st.session_state.filtros_aplicados = {
        "rango_anios": rango_anos,
        "meses": sel_meses,
        "dias": sel_dias,
        "departamento": sel_depto if sel_depto != "(Todos)" else None,
        "municipios": sel_muni,
        "sexos": sel_sexo,
        "grupos_edad": sel_edad,
        "mecanismos": sel_mec,
        "estado_civil": sel_estado_civil,
        "escolaridad": sel_escolaridad,
        "ancestro_racial": sel_ancestro
    }

filtros_estado = st.session_state.filtros_aplicados
df_act = aplicar_filtros_puros(df_clean, filtros_estado)
st.session_state['df_filtrado'] = df_act

# =============================================
# 📈 DASHBOARD ANALÍTICO
# =============================================

st.subheader("📈 Dashboard Analítico")

if df_act is None or df_act.empty:
    st.warning("⚠️ La combinación de filtros arroja **0 registros**. Sé más flexible en tu búsqueda.")
    st.stop()

# --- AYUDANTES DE SÍNTESIS ---
def calcular_top(df, col):
    """Devuelve la categoría más frecuente y su porcentaje."""
    if col not in df.columns: return "N/A", 0
    serie = df[col].dropna()
    if serie.empty: return "N/A", 0
    top = serie.mode().iloc[0]
    perc = (serie.value_counts().iloc[0] / len(serie)) * 100
    return top, perc

# --- KPIs DIRECTOS ---
top_depto, perc_depto = calcular_top(df_act, "Departamento del hecho DANE")
top_meca, perc_meca = calcular_top(df_act, "Mecanismo Causal de la Lesión Fatal")

k1, k2, k3 = st.columns(3)
k1.metric("📄 Total de Registros", f"{df_act.shape[0]:,}")
k2.metric("📌 Departamento Más Afectado", top_depto, f"{perc_depto:.1f}% de concentración")
k3.metric("⚠️ Mecanismo Principal", top_meca, f"{perc_meca:.1f}% del total")

st.divider()

# --- SECCIONES DE VISUALIZACIÓN ---
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

# DISTRIBUCIÓN POR SEXO
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

# CASOS POR MES Y DÍA
colC, colD = st.columns(2)

with colC:
    st.subheader("Casos por Mes del Año")
    if "Mes del hecho" in df_act.columns:
        df_mes = df_act.groupby("Mes del hecho").size().reset_index(name="Casos")
        chart_mes = alt.Chart(df_mes).mark_bar(color="#9B59B6").encode(
            x=alt.X("Mes del hecho:N", title="Mes", sort=None),
            y=alt.Y("Casos:Q"),
            tooltip=["Mes del hecho", "Casos"]
        ).properties(height=320)
        st.altair_chart(chart_mes, use_container_width=True)

with colD:
    st.subheader("Casos por Día de la Semana")
    if "Dia del hecho" in df_act.columns:
        df_dia = df_act.groupby("Dia del hecho").size().reset_index(name="Casos")
        chart_dia = alt.Chart(df_dia).mark_bar(color="#E74C3C").encode(
            x=alt.X("Dia del hecho:N", title="Día", sort=None),
            y=alt.Y("Casos:Q"),
            tooltip=["Dia del hecho", "Casos"]
        ).properties(height=320)
        st.altair_chart(chart_dia, use_container_width=True)

st.divider()

# ESTADO CIVIL Y ESCOLARIDAD
colE, colF = st.columns(2)

with colE:
    st.subheader("Casos por Estado Civil")
    if "Estado Civil" in df_act.columns:
        df_ec = df_act.groupby("Estado Civil").size().reset_index(name="Casos").sort_values("Casos", ascending=False)
        chart_ec = alt.Chart(df_ec).mark_bar(color="#1ABC9C").encode(
            x=alt.X("Casos:Q"),
            y=alt.Y("Estado Civil:N", sort="-x", title=""),
            tooltip=["Estado Civil", "Casos"]
        ).properties(height=320)
        st.altair_chart(chart_ec, use_container_width=True)

with colF:
    st.subheader("Casos por Escolaridad")
    if "Escolaridad" in df_act.columns:
        df_esc = df_act.groupby("Escolaridad").size().reset_index(name="Casos").sort_values("Casos", ascending=False)
        chart_esc = alt.Chart(df_esc).mark_bar(color="#F39C12").encode(
            x=alt.X("Casos:Q"),
            y=alt.Y("Escolaridad:N", sort="-x", title=""),
            tooltip=["Escolaridad", "Casos"]
        ).properties(height=320)
        st.altair_chart(chart_esc, use_container_width=True)

st.divider()

# ANCESTRO RACIAL
st.subheader("Casos por Ancestro Racial")
if "Ancestro Racial" in df_act.columns:
    df_anc = df_act.groupby("Ancestro Racial").size().reset_index(name="Casos").sort_values("Casos", ascending=False)
    chart_anc = alt.Chart(df_anc).mark_bar(color="#3498DB").encode(
        x=alt.X("Casos:Q"),
        y=alt.Y("Ancestro Racial:N", sort="-x", title=""),
        tooltip=["Ancestro Racial", "Casos"]
    ).properties(height=350)
    st.altair_chart(chart_anc, use_container_width=True)

st.divider()

# DEPARTAMENTOS
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

# --- EXPORTACIÓN LIMPIA ---
st.download_button(
    label="🔽 Exportar Conjunto de Datos Actual (CSV)",
    data=df_act.to_csv(index=False).encode('utf-8'),
    file_name="analisis_suicidios_filtrado.csv",
    mime="text/csv",
    use_container_width=True
)

st.divider()

# =============================================
# 📑 VISTA SEGMENTADA (AL FINAL)
# =============================================
st.subheader(f"📑 Vista Segmentada (Total Extraído: {df_act.shape[0]})")
st.dataframe(df_act.head(40), use_container_width=True)