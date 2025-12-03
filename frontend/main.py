import streamlit as st
import sys
from pathlib import Path

# Agregar el directorio parent al path para importar el api_client
sys.path.append(str(Path(__file__).parent))

from components.api_client import APIClient

# Configuración de la página
st.set_page_config(
    page_title="Game Database Manager",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inicializar cliente API
api = APIClient()

# Header principal
st.title("🎮 Gestor de Base de Datos del Juego")
st.markdown("### ¡Bienvenido! Administra tu mundo RPG desde aquí")

st.markdown("---")

# ==================== VERIFICACIÓN DE CONEXIÓN ====================
col1, col2, col3 = st.columns(3)

# Verificar que todo está funcionando
try:
    test_connection = api.get_players()
    system_ok = "error" not in test_connection
except:
    system_ok = False

with col1:
    if system_ok:
        st.success("✅ **Sistema Activo**")
    else:
        st.error("❌ **Sistema Inactivo**")

with col2:
    if system_ok:
        players_count = len(test_connection.get("players", []))
        st.info(f"👥 **{players_count} Jugadores**")
    else:
        st.info("👥 **-- Jugadores**")

with col3:
    st.info("🎮 **Versión 1.0**")

if not system_ok:
    st.error("⚠️ No se puede conectar al sistema. Por favor, contacta al administrador.")
    st.stop()

# Botón de refresco
if st.button("🔄 Actualizar", use_container_width=True):
    st.rerun()

st.markdown("---")

# ==================== GUÍA RÁPIDA ====================
st.header("🚀 Comienza Aquí")

st.markdown(
    """
Usa el **menú lateral** (←) para navegar entre las diferentes secciones:
"""
)

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
    ### 👤 Gestión Principal
    
    **👥 Players**  
    Administra los jugadores registrados
    
    **🦸 Characters**  
    Crea y gestiona personajes
    
    **⚔️ Items**  
    Catálogo de objetos del juego
    
    **🎯 Missions**  
    Sistema de misiones disponibles
    """
    )

with col2:
    st.markdown(
        """
    ### 📦 Gestión Avanzada
    
    **💱 Transactions**  
    Intercambios entre personajes
    
    **🎒 Inventory**  
    Inventario de cada personaje
    
    **🎯 Character Missions**  
    Asignar misiones a personajes
    
    **📊 Reports**  
    Ver estadísticas y análisis
    """
    )

st.markdown("---")

# ==================== PASOS RÁPIDOS ====================
st.header("📝 Pasos Rápidos para Empezar")

st.markdown(
    """
1. **Crea un Jugador** en la sección "Players"
2. **Crea un Personaje** asociado a ese jugador en "Characters"
3. **Agrega Items** en la sección "Items"
4. **Asigna Items** al inventario del personaje en "Inventory"
5. **Crea Misiones** en "Missions"
6. **Asigna Misiones** a tu personaje en "Character Missions"
7. **Consulta Reportes** para ver estadísticas en "Reports"
"""
)

st.markdown("---")

# ==================== ESTADÍSTICAS DEL JUEGO ====================
st.header("📊 Tu Mundo de Juego")

try:
    # Obtener datos
    players = api.get_players()
    characters = api.get_characters()
    items = api.get_items()
    missions = api.get_missions()
    transactions = api.get_transactions()

    # Mostrar métricas
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("👥 Jugadores", len(players.get("players", [])))

    with col2:
        st.metric("🦸 Personajes", len(characters.get("characters", [])))

    with col3:
        st.metric("⚔️ Items", len(items.get("items", [])))

    with col4:
        st.metric("🎯 Misiones", len(missions.get("missions", [])))

    with col5:
        st.metric("💱 Intercambios", len(transactions.get("transactions", [])))

    # Información adicional
    if len(characters.get("characters", [])) > 0:
        st.markdown("---")
        st.subheader("🏆 Personajes Destacados")

        # Ordenar personajes por nivel
        chars_list = characters.get("characters", [])
        chars_sorted = sorted(chars_list, key=lambda x: x["Level"], reverse=True)[:3]

        cols = st.columns(3)
        for idx, char in enumerate(chars_sorted):
            with cols[idx]:
                st.info(
                    f"""
                **{char['Name']}**  
                Nivel: {char['Level']}  
                Exp: {char['Experience']}
                """
                )

except Exception as e:
    st.warning(
        "No hay datos disponibles todavía. ¡Comienza creando jugadores y personajes!"
    )

st.markdown("---")

# ==================== CONSEJOS ÚTILES ====================
st.header("💡 Consejos Útiles")

tip1, tip2 = st.columns(2)

with tip1:
    st.info(
        """
    **✨ Tip #1: Orden de Creación**
    
    Siempre crea en este orden:
    1. Jugadores primero
    2. Luego personajes
    3. Después items y misiones
    4. Finalmente asignaciones
    """
    )

with tip2:
    st.warning(
        """
    **⚠️ Importante**
    
    - Al eliminar un jugador se eliminan sus personajes
    - Las transacciones necesitan 2 personajes
    - Usa el botón de actualizar para ver cambios
    """
    )

st.markdown("---")
