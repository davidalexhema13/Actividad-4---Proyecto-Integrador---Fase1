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
Configura un entorno de búsqueda granular. A diferencia del modo reactivo, aquí debes presionar **Aplicar Filtros** para salvaguardar el rendimiento debido al volumen de datos. El sistema se encarga internamente de normalizar y pulir las entradas (pipeline de validación).
""")

# 🔄 BOTÓN PARA FORZAR RECARGA
if st.button("🔄 Recargar datos (forzar pipeline)"):
    st.session_state.pop("df_raw", None)
    st.session_state.pop("df_filtrado", None)
    st.rerun()

# INICIALIZACIÓN DE ESTADOS
if "filtros_config" not in st.session_state:
    st.session_state.filtros_config = {}

# 🔥 CARGA CON DEBUG (SIN CACHE ROTO)
with st.spinner("Cargando y validando Pipeline base..."):
    try:
        df = cargar_datos()
        df_validado = pipeline_validacion(df)
        st.session_state.df_raw = df_validado
    except Exception as e:
        st.error(f"💥 ERROR REAL EN PIPELINE: {e}")
        st.stop()

df_clean = st.session_state.df_raw

def resetear_filtros():
    st.session_state.filtros_config = {}
    st.session_state.df_filtrado = df_clean.copy() if df_clean is not None else None
    st.toast("Filtros restablecidos", icon="🧹")

if df_clean is not None and not df_clean.empty:
    st.info(f"💾 Se ha cargado el modelo base pre-validado con **{df_clean.shape[0]}** registros íntegros.")
    
    # -----------------------------
    # CONSTRUCCIÓN DE LA UI (PANEL)
    # -----------------------------
    
    with st.form("panel_filtros_form"):
        st.subheader("Arquitectura de Filtros")
        
        col1, col2, col3 = st.columns(3)
        
        # COL 1: Espacio-Temporal
        with col1:
            st.markdown("#### ⏳ Dimensión Espacio-Temporal")
            
            min_y = int(df_clean["Año del hecho"].min())
            max_y = int(df_clean["Año del hecho"].max())
            def_y = st.session_state.filtros_config.get("rango_anios", (min_y, max_y))
            rango_anos = st.slider("Rango de Años:", min_y, max_y, def_y)
            
            if "Mes del hecho" in df_clean.columns:
                meses_uni = df_clean["Mes del hecho"].dropna().unique().tolist()
                def_m = st.session_state.filtros_config.get("meses", [])
                sel_meses = st.multiselect("Meses de Registro:", meses_uni, default=def_m)
            else:
                sel_meses = []

        # COL 2: Geografía Relacional
        with col2:
            st.markdown("#### 🗺️ Dimensión Geográfica")
            
            if "Departamento del hecho DANE" in df_clean.columns:
                deptos_uni = sorted(df_clean["Departamento del hecho DANE"].dropna().unique().tolist())
                
                def_d_index = 0
                if "departamento" in st.session_state.filtros_config and st.session_state.filtros_config["departamento"] in deptos_uni:
                    def_d_index = deptos_uni.index(st.session_state.filtros_config["departamento"]) + 1
                
                opciones_dpt = ["(Todos)"] + deptos_uni
                sel_depto = st.selectbox("Seleccione Departamento:", opciones_dpt, index=def_d_index)

                sel_muni = []
                if sel_depto != "(Todos)" and "Municipio del hecho DANE" in df_clean.columns:
                    muni_filtrados = df_clean[df_clean["Departamento del hecho DANE"] == sel_depto]
                    muni_uni = sorted(muni_filtrados["Municipio del hecho DANE"].dropna().unique().tolist())
                    
                    def_mun = [m for m in st.session_state.filtros_config.get("municipios", []) if m in muni_uni]
                    sel_muni = st.multiselect("Municipios (relacionado):", muni_uni, default=def_mun)
            else:
                sel_depto = "(Todos)"
                sel_muni = []

        # COL 3: Contexto / Demografía
        with col3:
            st.markdown("#### 👥 Dimensión Causal / Demográfica")
            
            if "Sexo de la victima" in df_clean.columns:
                sex_uni = sorted(df_clean["Sexo de la victima"].dropna().unique().tolist())
                sel_sexo = st.multiselect("Género/Sexo:", sex_uni, default=st.session_state.filtros_config.get("sexos", sex_uni))
            else:
                sel_sexo = []
                
            if "Grupo de Edad Quinquenal " in df_clean.columns:
                edad_uni = sorted(df_clean["Grupo de Edad Quinquenal "].dropna().unique().tolist())
                sel_edad = st.multiselect("Grupo Etario:", edad_uni, default=st.session_state.filtros_config.get("grupos_edad", []))
            else:
                sel_edad = []
                
            if "Mecanismo Causal de la Lesión Fatal" in df_clean.columns:
                mec_uni = sorted(df_clean["Mecanismo Causal de la Lesión Fatal"].dropna().unique().tolist())
                sel_mec = st.multiselect("Mecanismo Causal:", mec_uni, default=st.session_state.filtros_config.get("mecanismos", []))
            else:
                sel_mec = []

        st.divider()
        cmd_col1, cmd_col2, cmd_col3 = st.columns([1,1,2])
        
        with cmd_col1:
            submit_btn = st.form_submit_button("✅ Aplicar Filtros (Puros)", use_container_width=True)
        with cmd_col2:
            clear_btn = st.form_submit_button("🗑️ Limpiar Configuración", use_container_width=True)
            
    if clear_btn:
        resetear_filtros()
        st.rerun()
        
    if submit_btn:
        nuevo_estado = {
            "rango_anios": rango_anos,
            "meses": sel_meses,
            "departamento": sel_depto if sel_depto != "(Todos)" else None,
            "municipios": sel_muni,
            "sexos": sel_sexo,
            "grupos_edad": sel_edad,
            "mecanismos": sel_mec
        }
        st.session_state.filtros_config = nuevo_estado
        
        with st.spinner("⏳ Vectorizando y acotando el Dataset basado en presets de sesión..."):
            df_res = aplicar_filtros_puros(df_clean, nuevo_estado)
            st.session_state['df_filtrado'] = df_res
            st.success("Configuración aplicada exitosamente.")

    if "df_filtrado" in st.session_state and st.session_state.df_filtrado is not None:
         df_f = st.session_state.df_filtrado
         if df_f.empty:
             st.warning("⚠️ La combinación de filtros arroja **0 registros**. El sistema está estable, pero te invitamos a ser más flexible en tu búsqueda.")
         else:
             st.subheader(f"📑 Vista Segmentada (Total Extraído: {df_f.shape[0]})")
             st.dataframe(df_f.head(40), use_container_width=True)

else:
    st.error("🚫 Ocurrió un error en el origen de los datos o el pipeline destruyó el contenido (posible csv corrupto).")

# =============================================
# 📈 DASHBOARD ANALÍTICO (EX MÓDULO 4)
# =============================================

st.divider()
st.title("📈 Dashboard Analítico: Presuntos Suicidios en Colombia")

# --- 1. CARGA DE DATOS CENTRALIZADA ---
# Se simplifica el flujo priorizando los datos del Módulo 3. Si no existen, carga el general.
@st.cache_data(show_spinner=False)
def cargar_fuente_fallback():
    return pipeline_validacion(cargar_datos())

if "df_filtrado" in st.session_state and st.session_state["df_filtrado"] is not None:
    df_act = st.session_state["df_filtrado"]
    st.sidebar.success("✅ Mostrando datos filtrados.")
else:
    df_act = cargar_fuente_fallback()
    st.sidebar.info("💡 Mostrando base de datos global. Aplica filtros arriba para segmentar.")

if df_act is None or df_act.empty:
    st.warning("📉 El conjunto de datos está vacío. Ajusta los filtros arriba.")
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