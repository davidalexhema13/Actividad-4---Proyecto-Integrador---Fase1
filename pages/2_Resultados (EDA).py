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
       placeholder="Contiene información prevalente de los presuntos suicidios ocurridos en el territorio nacional Colombiano en el periodo de tiempo comprendido entre los años 2015 a 2024 de los cuales tiene conocimiento y son registrados por el Instituto Nacional de Medicina Legal y Ciencias Forenses.",
       height=150
   )

   st.header("❗ 2. Calidad de los Datos")
   calidad = st.text_area(
       "¿Qué encontraste sobre los datos faltantes y la limpieza?",
       placeholder="""Se observo que:,
                La columna 'Pertenencia Étnica' tiene un 33% de datos sin información y un  65% de datos sin pertenencia étnica.,
                La columna 'Localidad del hecho' tiene un 86% de datos sin información.
                La columna 'Mes del hecho' tiene un 22% de datos en donde se desconoce el mes.
                La columna 'Municipio del hecho DANE' tiene un 64% de datos en donde se desconoce el municipio.
                La columna 'Orientación sexual' tiene un 66% de información no implementada y un 19% no sabe/ no informa.
                La columna 'Pueblo indígena'  tiene un 26% de información no implementada.
                La columna 'Rango de Hora del Hecho X 3 Horas' tiene un 60% de datos sin información y un 6 % de datos  'otro'.
                La columna 'Razón del Suicidio' tiene un 53% de datos sin información.
                La columna 'Transgénero' tiene un 66%  de datos no implementados y un 34% no sabe / no informa.
            """,
       height=150
   )

   st.header("📈 3. Hallazgos Estadísticos Key")
   estadisticas = st.text_area(
       "Interpretación de los números y categorías principales (Medias, modas, etc.)",
        placeholder="""
            - El perfil típico de una víctima de suicidio en Colombia durante el período 2015-2024 es: hombre, adulto (29-59 años), soltero,con bajo nivel      educativo, que utiliza ahorcamiento y lo hace en su vivienda, generalmente por conflictos de pareja o enfermedades.

             - Proyectil de arma de fuego: Es un método con una presencia constante, lo que puede estar relacionado con contextos de conflicto, pertenencia a fuerzas armadas o simplemente acceso a armas en zonas rurales.

            - Si bien la mayoría de los suicidios ocurren en cabeceras municipales (zonas urbanas), el porcentaje que ocurre en la parte rural (vereda y campo) es significativo y no debe ignorarse.
            
            - Indígenas y Negros/Mulatos: Aunque el mestizo es el grupo mayoritario, la presencia de víctimas de comunidades indígenas y afrocolombianas es constante.
            """,
       height=150
   )

   st.header("💡 4. Conclusión Final")
   conclusion = st.text_area(
       "¿Cuál es el mensaje principal que nos dan estos datos?",
       placeholder="El mensaje principal que nos da estos datos es la importancia y la relevancia acerca del suicidio en Colombia, esto nos permite sacar conclusiones sobre la salud mental de los colombianos",
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


