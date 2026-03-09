import streamlit as st
import pandas as pd


# Configuración de la página
st.set_page_config(page_title="Actividad: Descubriendo los Datos", layout="wide")

st.title("🧩 Actividad: ¿De qué se tratan estos datos?")
st.markdown("""
### Objetivo de la Actividad
Tu misión es actuar como un **detective de datos**. A partir de las tablas y estadísticas que verás a continuación, debes deducir el contexto, el origen y el propósito de este conjunto de datos.
""")

# --- Barra Lateral con Instrucciones ---
with st.sidebar:
   st.header("📋 Guía para el Estudiante")
   st.info("""
   1. **Previsualiza**: Observa las primeras filas. ¿Hay nombres de ciudades, fechas o categorías conocidas?
   2. **Inspecciona**: Mira las dimensiones. ¿Es un dataset pequeño o masivo?
   3. **Analiza Limpieza**: ¿Faltan muchos datos? ¿En qué columnas?
   4. **Deduce**: Usa las estadísticas para entender el 'comportamiento' de los datos.
   """)
   st.warning("⚠️ **Prohibido usar gráficos**. El reto es entender los datos solo con números y texto.")

# --- 1. Carga de Datos ---
uploaded_file = st.file_uploader("Sube un archivo CSV para investigar", type="csv")

@st.cache_data
def load_data(file):
   try:
       return pd.read_csv(file)
   except Exception as e:
       st.error(f"Error al cargar el archivo: {e}")
       return None

# Lógica de selección de archivo
df = None
if uploaded_file is not None:
   df = load_data(uploaded_file)
   if df is not None:
       st.success("🕵️ Dataset cargado para investigación.")

if df is not None:
   # --- Paso 1: Primer Impacto ---
   st.header("Step 1: 🔍 Primer Impacto (Dataset Preview)")
   st.markdown("Observa las primeras filas. ¿Qué conceptos o palabras clave se repiten?")
   st.dataframe(df.head(10))
   
   with st.expander("💡 ¿Cómo interpretar este paso?"):
       st.write("""
       - **Nombres de Columnas:** Son las 'etiquetas' de la información. Si ves 'Municipio', sabes que hay datos geográficos. Si ves 'Fecha', hay una línea de tiempo.
       - **Valores Iniciales:** Te dan una idea del formato. ¿Son números decimales, enteros, o texto largo?
       - **Identificadores:** Busca columnas como 'ID' o 'Código', suelen ser llaves únicas para cada registro.
       """)

   # --- Paso 2: La Estructura ---
   st.header("Step 2: 🏗️ La Estructura")
   col1, col2 = st.columns(2)
   with col1:
       st.subheader("¿Qué tan grande es?")
       st.write(f"Filas: **{df.shape[0]}**")
       st.write(f"Columnas: **{df.shape[1]}**")
   with col2:
       st.subheader("¿Qué tipos de datos hay?")
       st.write(df.dtypes)
   
   with st.expander("💡 ¿Cómo interpretar la estructura?"):
       st.write("""
       - **Filas:** Representan la cantidad de 'eventos' o 'sujetos' registrados. Miles de filas sugieren un fenómeno masivo o de largo plazo.
       - **Columnas:** Representan las 'características' medidas. Muchas columnas significan un análisis muy detallado.
       - **Tipos (dtypes):** 
           - `int64` / `float64`: Son números. Permiten sumas y promedios.
           - `object`: Generalmente es texto o categorías.
           - `datetime64`: Fechas y horas (esencial para ver tendencias en el tiempo).
       """)

   # --- Paso 3: Calidad y Vacíos ---
   st.header("Step 3: ❗ Calidad y Vacíos")
   missing = df.isnull().sum()
   if missing.sum() > 0:
       st.write("Columnas con datos faltantes:")
       st.write(missing[missing > 0])
       st.write("💡 *Pregunta: ¿Por qué crees que faltan datos en esas columnas específicas?*")
   else:
       st.success("¡Increíble! Este dataset está completo. No faltan datos.")
   
   with st.expander("💡 ¿Qué significan los datos faltantes?"):
       st.write("""
       - **Nulos (NaN):** Indican información que no se recolectó o no aplica.
       - **Impacto:** Si una columna importante (como 'Costo' o 'Fecha') tiene muchos nulos, tus conclusiones podrían ser poco confiables.
       - **Sesgo:** Si los datos solo faltan para ciertos grupos, el análisis podría estar inclinado hacia un lado.
       """)

   # --- Paso 4: El Corazón de los Datos ---
   st.header("Step 4: 📈 El Corazón de los Datos (Estadísticas)")
   
   tab1, tab2 = st.tabs(["Números (Cuantitativo)", "Categorías (Cualitativo)"])
   
   with tab1:
       st.write("Resumen estadístico de las columnas numéricas:")
       st.dataframe(df.describe())
       
       with st.expander("📊 Guía de Estadísticas Numéricas"):
           st.write("""
           - **Mean (Promedio):** El valor central. ¿Es lo que esperabas para este tema?
           - **Min / Max:** Los límites. Te ayudan a detectar 'outliers' (valores extraños o errores).
           - **Std (Desviación):** Qué tan 'dispersos' están los datos. Un número alto significa mucha variedad.
           - **50% (Mediana):** El punto medio exacto. Si es muy diferente al promedio, los datos están 'estirados' hacia un extremo.
           """)
       
   with tab2:
       cat_desc = df.describe(exclude=['number'])
       if not cat_desc.empty:
           st.write("Resumen de las columnas de texto/categorías:")
           st.dataframe(cat_desc)
           
           with st.expander("🔠 Guía de Estadísticas Categóricas"):
               st.write("""
               - **Unique:** Cuántas opciones diferentes hay (ej: 32 departamentos).
               - **Top (Moda):** El valor que más se repite. ¡Suele ser la clave del dataset!
               - **Freq:** Cuántas veces aparece el valor 'top'.
               """)
       else:
           st.write("No se detectaron columnas categóricas.")

   # --- Conclusiones de Investigación ---
   st.header("📝 Resumen de Hallazgos")
   
   num_cols = df.select_dtypes(include=['number']).columns.tolist()
   cat_cols = df.select_dtypes(exclude=['number']).columns.tolist()
   
   st.markdown(f"""
   ### 🕵️ Informe del Detective
   Basado en tu investigación, aquí hay una validación de lo que has encontrado:
   
   *   **Volumen**: Estás manejando **{df.shape[0]} registros**, lo que permite una visión {'global' if df.shape[0] > 1000 else 'específica'} del fenómeno.
   *   **Variables**: El dataset contiene **{len(cat_cols)} llaves de texto** que definen el 'qué' y el 'dónde', y **{len(num_cols)} llaves numéricas** compartiendo el 'cuánto'.
   *   **Contexto Sugerido**: Las columnas `{", ".join(cat_cols[:3])}...` sugieren que estamos analizando un fenómeno relacionado con la gestión, reportes o eventos en un entorno específico.
   
   **¿Lograste identificar de qué se trata exactamente el dataset?**
   """)
else:
   st.warning("Escribe o sube un archivo CSV para empezar el reto.")



