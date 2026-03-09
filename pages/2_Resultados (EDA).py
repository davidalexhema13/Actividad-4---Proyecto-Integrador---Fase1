import streamlit as st

# Configuración de la página
st.set_page_config(
   page_title="Plantilla de Resultados - Proyecto Analítica",
   page_icon="📝",
   layout="wide"
)

st.title("📝 Plantilla de Entrega: Resultados del EDA")
st.markdown("""
### Instrucciones
Utiliza esta página para documentar tus hallazgos. Completa cada sección basándote en lo que descubriste en la pestaña de **Análisis Exploratorio**.
Al finalizar, puedes previsualizar tu reporte consolidado.
""")

st.divider()

# --- Formulario de Resultados ---
with st.container():
   st.header("🔍 1. Identificación y Contexto")
   contexto = st.text_area(
       "¿De qué se trata el dataset? (Deducción del origen, tema y propósito)",
       placeholder="Ej: El dataset trata sobre accidentes de tránsito en Antioquia durante el año 2023...",
       height=150
   )

   st.header("❗ 2. Calidad de los Datos")
   calidad = st.text_area(
       "¿Qué encontraste sobre los datos faltantes y la limpieza?",
       placeholder="Ej: Se observó que la columna 'Causa' tiene un 20% de nulos, lo cual podría sesgar...",
       height=150
   )

   st.header("📈 3. Hallazgos Estadísticos Key")
   estadisticas = st.text_area(
       "Interpretación de los números y categorías principales (Medias, modas, etc.)",
       placeholder="Ej: La mayoría de incidentes ocurren en el municipio de Medellín (Moda) con un promedio diario de...",
       height=150
   )

   st.header("💡 4. Conclusión Final")
   conclusion = st.text_area(
       "¿Cuál es el mensaje principal que nos dan estos datos?",
       placeholder="Ej: El dataset revela una alta concentración de eventos en áreas urbanas...",
       height=100
   )

st.divider()

# --- Generación de Reporte ---
if st.button("🚀 Generar Previsualización del Reporte"):
   if contexto and calidad and estadisticas and conclusion:
       st.success("✅ Reporte Generado Exitosamente")
       
       reporte_md = f"""
       # Reporte de Análisis Exploratorio de Datos
       
       ## 1. Identificación y Contexto
       {contexto}
       
       ## 2. Calidad de los Datos
       {calidad}
       
       ## 3. Hallazgos Estadísticos Clave
       {estadisticas}
       
       ## 4. Conclusión Final
       {conclusion}
       
       ---
       *Generado por el módulo de Reportes - Proyecto Integrador*
       """
       
       st.markdown(reporte_md)
       st.download_button(
           label="📥 Descargar Reporte (.md)",
           data=reporte_md,
           file_name="reporte_eda_estudiante.md",
           mime="text/markdown"
       )
   else:
       st.warning("⚠️ Por favor, completa todas las secciones antes de generar el reporte.")

# --- Barra Lateral ---
st.sidebar.info("Esta es tu hoja de trabajo. Asegúrate de analizar bien los datos antes de escribir tus conclusiones.")
st.sidebar.markdown("---")
st.sidebar.write("© 2026 - Plantilla de Resultados")


