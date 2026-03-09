import streamlit as st

# Configuración de la página
st.set_page_config(
   page_title="Proyecto Integrador - Analítica de Datos",
   page_icon="🚀",
   layout="wide",
   initial_sidebar_state="expanded"
)

# --- Estilo Personalizado (Opcional) ---
st.markdown("""
   <style>
   .main {
       background-color: #f8f9fa;
   }
   .stAlert {
       border-radius: 10px;
   }
   </style>
   """, unsafe_allow_html=True)

# --- Título Principal ---
st.title("🚀 Proyecto Integrador: Analítica de Datos")
st.subheader("Transformando Información en Decisiones Estratégicas")

st.divider()

# --- 1. Introducción ---
col1, col2 = st.columns([2, 1])

with col1:
   st.header("📖 Introducción")
   st.write("""
   El análisis de datos se ha convertido en una herramienta fundamental para comprender fenómenos sociales y apoyar la toma de decisiones basada en evidencia. En el contexto colombiano, el estudio de las lesiones de causa externa, como los presuntos suicidios, representa un tema de gran relevancia para la salud pública, las políticas sociales y la prevención de riesgos en la población.

El presente proyecto tiene como objetivo analizar el conjunto de datos “Presuntos Suicidios en Colombia 2015–2024”, publicado por el Instituto Nacional de Medicina Legal y Ciencias Forenses. Este dataset contiene información estadística sobre casos registrados por el sistema médico legal colombiano durante el periodo comprendido entre los años 2015 y 2024.

Para el desarrollo del análisis se utilizaron herramientas de ciencia de datos en Python, particularmente la librería pandas para la manipulación, limpieza y análisis de los datos, y la plataforma Streamlit para la construcción de una aplicación interactiva que permite visualizar la información de manera dinámica mediante tablas, gráficos y filtros.

Es importante señalar que la información presentada corresponde a presuntos suicidios, es decir, casos clasificados con base en criterios forenses y registros institucionales, sin que ello implique una determinación judicial sobre las circunstancias definitivas de cada evento. Por lo tanto, los resultados del análisis deben interpretarse como una aproximación estadística que permite identificar patrones, tendencias y posibles factores asociados a este fenómeno en el territorio colombiano.
   """)

with col2:
   st.info("💡 **Dato Curioso:** El 80% del trabajo de un analista de datos se dedica a la limpieza y preparación de la información.")

# --- 2. Objetivos ---
st.header("🎯 Objetivos del Proyecto")

obj_gen, obj_esp = st.columns(2)

with obj_gen:
   st.subheader("Objetivo General")
   st.markdown("""
   - Analizar y visualizar los datos de presuntos suicidios registrados en Colombia entre los años 2015 y 2024 mediante el uso de herramientas de ciencia de datos en Python, utilizando pandas para el procesamiento de la información y Streamlit para la construcción de una aplicación interactiva que facilite la exploración y comprensión de los datos.
   """)

with obj_esp:
   st.subheader("Objetivos Específicos")
   st.markdown("""
 - Explorar y comprender el conjunto de datos, identificando sus variables, estructura y características principales.

- Realizar procesos de limpieza y transformación de datos utilizando la librería pandas, con el fin de preparar la información para su análisis.

- Analizar tendencias y patrones estadísticos relacionados con los presuntos suicidios en Colombia durante el periodo 2015–2024.

- Desarrollar una aplicación interactiva con Streamlit que permita a los usuarios explorar los datos mediante filtros.
   """)

st.divider()

# --- 3. Equipo de Trabajo ---
st.header("👥 Equipo de Trabajo (Integrantes)")

# Puedes ajustar los nombres aquí
integrantes = [
   {"nombre": "Daruin Montoya Quiroz", "rol": "Analista de Datos", "emoji": "👨‍💻"},
   {"nombre": "Luis Esteban Rodriguez", "rol": "Ingeniero de Datos", "emoji": "👩‍🔬"},
   {"nombre": "Daniel Esteban Hurtado", "rol": "Arquitecto de Soluciones", "emoji": "👨‍💼"},
   {"nombre": "David Alexander Machado", "rol": "Especialista en Machine Learning", "emoji": "🏃‍♂️"},
]

cols = st.columns(len(integrantes))

for i, persona in enumerate(integrantes):
   with cols[i]:
       st.markdown(f"""
       ### {persona['emoji']} {persona['nombre']}
       **Roles:** {persona['rol']}
       """)

st.divider()

# --- 4. Tecnologías Utilizadas ---
st.header("🛠️ Tecnologías")

tech_col1, tech_col2, tech_col3 = st.columns(3)

with tech_col1:
   st.markdown("### 🐍 Python")
   st.write("Lenguaje base para el procesamiento y lógica del proyecto.")

with tech_col2:
   st.markdown("### 🐼 Pandas")
   st.write("Librería líder para manipulación y análisis de estructuras de datos.")

with tech_col3:
   st.markdown("### 🎈 Streamlit")
   st.write("Framework para la creación de aplicaciones web interactivas de datos.")

# --- Pie de página ---
st.sidebar.success("👈 Usa el menú lateral para navegar entre las secciones del proyecto.")
st.sidebar.markdown("---")
st.sidebar.write("© 2026 - Proyecto Integrador de Analítica")



