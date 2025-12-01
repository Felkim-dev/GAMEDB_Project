import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Game Database Manager",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Página principal
st.title("🎮 Game Database Manager")
st.markdown("---")

st.header("Bienvenido al Sistema de Gestión de Base de Datos de Videojuegos")

st.markdown(
    """
### 📊 Funcionalidades disponibles:

Usa el menú de la izquierda para navegar entre las diferentes secciones:

- **👥 Players** - Gestiona los jugadores registrados
- **🦸 Characters** - Administra los personajes de cada jugador
- **⚔️ Items** - Catálogo de items disponibles
- **💱 Transactions** - Registro de transacciones entre personajes
- **🎒 Inventory** - Gestión de inventarios de personajes
- **🎯 Missions** - Sistema de misiones
- **🎯 Character Missions** - Asignación de misiones a personajes

### 🚀 Instrucciones:

1. Asegúrate de que la API Flask esté corriendo en `http://localhost:5000`
2. Asegúrate de que el contenedor Docker de MySQL esté activo
3. Navega por las páginas usando el menú lateral
4. Comienza creando jugadores, luego personajes, y después items/misiones

### 📝 Estado del Sistema:
"""
)

# Verificar conexión con API
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("API Status", "🔴 Verificando...")

with col2:
    st.metric("Database Status", "🔴 Verificando...")

with col3:
    st.metric("Frontend Version", "1.0.0")

st.markdown("---")

st.info(
    "💡 **Consejo:** Comienza por la sección de Players para crear jugadores y luego crea personajes asociados."
)
