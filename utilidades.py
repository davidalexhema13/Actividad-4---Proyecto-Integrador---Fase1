import pandas as pd
import streamlit as st
import os

@st.cache_data(show_spinner=False)
def cargar_datos():
    """
    Carga los datos en bruto desde el archivo CSV principal.
    Aprovecha caché de Streamlit para no releer del disco a cada recarga.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "datos.csv")
    
    if not os.path.exists(file_path):
        st.error(f"❌ CSV no encontrado en: {file_path}")
        return None
    try:
        return pd.read_csv(file_path, low_memory=False)
    except Exception as e:
        st.error(f"Error cargando los datos: {str(e)}")
        return None

@st.cache_data(show_spinner=False)
def pipeline_validacion(df):
    """
    Capa de Data Pipeline: Limpieza estricta y normalización de tipos.
    Garantiza consistencia para evitar roturas en filtros dinámicos y visualizaciones críticas.
    """
    if df is None or df.empty:
        return df
        
    df_clean = df.copy()
    
    # 1. Eliminar duplicados absolutos
    df_clean = df_clean.drop_duplicates()
    
    # 2. Casteo de Tipos Estrictos
    if "Año del hecho" in df_clean.columns:
        df_clean["Año del hecho"] = pd.to_numeric(df_clean["Año del hecho"], errors="coerce").astype("Int64")
        
    # 3. Normalización de textos para homogeneizar datos (ej. quitar espacios espurios)
    obj_cols = df_clean.select_dtypes(include='object').columns
    for col in obj_cols:
        df_clean[col] = df_clean[col].astype(str).str.strip()
        # Normalizar strings tipo 'Sin información' / 'nan' como nulos reales para evitar falsos positivos
        df_clean[col] = df_clean[col].replace(["Sin información", "Sin Información", "nan", "<NA>", "None"], pd.NA)

    # 4. Limpieza estricta de vacíos estructurales
    # Validamos que el registro posea integridad en las columnas vitales del dashboard.
    columnas_clave = ["Año del hecho", "Departamento del hecho DANE", "Sexo de la victima", "Mecanismo Causal de la Lesión Fatal", "Grupo de Edad Quinquenal "]
    columnas_presentes = [c for c in columnas_clave if c in df_clean.columns]
    
    if columnas_presentes:
        df_clean = df_clean.dropna(subset=columnas_presentes)
        
    return df_clean

@st.cache_data(show_spinner=False)
def aplicar_filtros_puros(df, filtros_estado: dict):
    """
    Lógica pura: recibe un DataFrame validado y un diccionario estricto de filtros,
    computa intersecciones y retorna la vista acotada. 
    100% independiente del ciclo de vida interactivo de UI Streamlit.
    """
    if df is None or df.empty or not filtros_estado:
        return df

    df_filtrado = df.copy()

    # 1. Filtro Espacio-Temporal
    if "rango_anios" in filtros_estado and "Año del hecho" in df.columns:
        min_y, max_y = filtros_estado["rango_anios"]
        df_filtrado = df_filtrado[(df_filtrado["Año del hecho"] >= min_y) & (df_filtrado["Año del hecho"] <= max_y)]

    if filtros_estado.get("meses") and "Mes del hecho" in df.columns:
        df_filtrado = df_filtrado[df_filtrado["Mes del hecho"].isin(filtros_estado["meses"])]

    # 2. Filtro Geográfico y Dependiente
    if filtros_estado.get("departamento") and "Departamento del hecho DANE" in df.columns:
        df_filtrado = df_filtrado[df_filtrado["Departamento del hecho DANE"] == filtros_estado["departamento"]]
        
        if filtros_estado.get("municipios") and "Municipio del hecho DANE" in df.columns:
            df_filtrado = df_filtrado[df_filtrado["Municipio del hecho DANE"].isin(filtros_estado["municipios"])]

    # 3. Filtros Demográficos
    if filtros_estado.get("sexos") and "Sexo de la victima" in df.columns:
        df_filtrado = df_filtrado[df_filtrado["Sexo de la victima"].isin(filtros_estado["sexos"])]

    if filtros_estado.get("grupos_edad") and "Grupo de Edad Quinquenal " in df.columns:
        df_filtrado = df_filtrado[df_filtrado["Grupo de Edad Quinquenal "].isin(filtros_estado["grupos_edad"])]

    # 4. Filtros Relacionados al Evento Causante
    if filtros_estado.get("mecanismos") and "Mecanismo Causal de la Lesión Fatal" in df.columns:
        df_filtrado = df_filtrado[df_filtrado["Mecanismo Causal de la Lesión Fatal"].isin(filtros_estado["mecanismos"])]
        
    if filtros_estado.get("razon") and "Razón del Suicidio" in df.columns:
        df_filtrado = df_filtrado[df_filtrado["Razón del Suicidio"].isin(filtros_estado["razon"])]

    return df_filtrado