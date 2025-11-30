import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Agregar el directorio parent al path para importar el api_client
sys.path.append(str(Path(__file__).parent.parent))

from components.api_client import APIClient

# Configuración de la página
st.set_page_config(page_title="Character", page_icon="🦸", layout="wide")

# Inicializar cliente API
api = APIClient()

st.title("🦸 Gestión de Personajes")
st.markdown("---")

# Tabs para diferentes acciones
tab1, tab2, tab3 = st.tabs(
    ["📋 Ver Personajes", "➕ Crear Personaje", "✏️ Editar/Eliminar"]
)

# ==================== TAB 1: VER PERSONAJES ====================
with tab1:
    st.header("Lista de Personajes")

    if st.button("🔄 Actualizar Lista", key="refresh_characters"):
        st.rerun()

    characters = api.get_characters()

    if "error" in characters:
        st.error(f"❌ Error al cargar jugadores: {characters['error']}")
    elif not characters["characters"]:
        st.info("ℹ️ No hay jugadores registrados todavía.")
    else:

        df = pd.DataFrame(characters['characters'])
        # Cambia este orden según tu preferencia
        column_order = ["CharacterID", "PlayerID", "Name", "Level", "Experience"]
        df = df[column_order]

        # Mostrar jugadores en formato de tabla
        st.dataframe(
            df,
            width="stretch",
            hide_index=True,
        )

        st.success(f"✅ Total de jugadores: {len(characters['characters'])}")

# ==================== TAB 2: CREAR PERSONAJE ====================
with tab2:
    st.header("Crear Nuevo Personaje")

    players = api.get_players()
    
    with st.form("create_personajes_form"):
        col1, col2 = st.columns(2)

        with col1:
            
            if "error" not in players and players["players"]:

                # Selector de jugador
                player_options = {
                    f"{p['PlayerID']} - {p['UserName']}": p["PlayerID"]
                    for p in players["players"]
                }
                selected_player = st.selectbox(
                    "Selecciona un jugador:", options=list(player_options.keys())
                )

                if selected_player:
                    player_id = player_options[selected_player]

        with col2:
            character_name = st.text_input("Nombre de Personaje*", placeholder="usuario123")

        submitted = st.form_submit_button("➕ Crear Personaje", width='stretch')

        if submitted:
            if not character_name:
                st.error("❌ Todos los campos marcados con * son obligatorios")
            else:
                # Preparar datos
                character_data = {
                    "PlayerID": player_id,
                    "Name": character_name,
                    "Level": 1,
                    "Experience": 0
                }

                # Llamar a la API
                result = api.create_character(character_data)
                
                if "error" in result:
                    st.error(f"❌ Error: {result['error']}")
                else:
                    st.success("✅ Personaje creado exitosamente!")
                    st.balloons()
                    st.json(result)

# ==================== TAB 3: EDITAR/ELIMINAR ====================
with tab3:
    st.header("Editar o Eliminar Personaje")

    players = api.get_players()

    if "error" not in players and players["players"]:

        # Selector de jugador
        player_options = {
            f"{p['PlayerID']} - {p['UserName']}": p["PlayerID"]
            for p in players["players"]
        }
        selected_player = st.selectbox(
            "Selecciona un jugador:", options=list(player_options.keys())
        )

        characters = api.get_characters()

        if "error" not in characters and characters["characters"]:

            selected_characters = []

            for character in characters["characters"]:

                if character["PlayerID"] == player_options[selected_player]:
                    selected_characters.append(character) 

            if not selected_characters:
                st.info("ℹ️ No hay personajes disponibles para este usuario.")

            else:
                character_options = {
                    f"{p['CharacterID']} - {p['Name']}": p["CharacterID"]
                    for p in selected_characters
                }

                selected_character = st.selectbox(
                "Selecciona un personaje:",
                options=list(character_options.keys()),
                )

                if selected_character:
                    character_id = character_options[selected_character]
                    character_detail = api.get_character(character_id)

                    if "error" not in character_detail and selected_characters:
                        col1, col2 = st.columns(2)

                        # Columna 1: Editar
                        with col1:
                            st.subheader("✏️ Editar Personaje")

                            with st.form("edit_character_form"):

                                new_name = st.text_input(
                                    "Nombre", value=character_detail.get("Name", "")
                                )
                                new_level = st.text_input(
                                    "Nivel", value=character_detail.get("Level", "")
                                )

                                update_submitted = st.form_submit_button(
                                    "💾 Actualizar", width="stretch"
                                )

                                if update_submitted:
                                    updated_data = {
                                        "Name": new_name,
                                        "Level": new_level,
                                        "Experience" : str((int(new_level)*1000))
                                    }

                                    result = api.update_character(character_id, updated_data)

                                    if "error" in result:
                                        st.error(f"❌ Error: {result['error']}")
                                    else:
                                        st.success("✅ Personaje actualizado exitosamente!")
                                        st.rerun()

                        # Columna 2: Eliminar
                        with col2:
                            st.subheader("🗑️ Eliminar Personaje")
                            st.warning(
                                "⚠️ Esta acción no se puede deshacer."
                            )

                            confirm = st.checkbox("Confirmo que quiero eliminar este personaje")

                            if st.button(
                                "🗑️ Eliminar personaje",
                                disabled=not confirm,
                                width="stretch",
                            ):
                                result = api.delete_character(character_id)

                                if "error" in result:
                                    st.error(f"❌ Error: {result['error']}")
                                else:
                                    st.success("✅ Jugador eliminado exitosamente!")
                                    st.rerun()
                    else:
                        st.error(f"❌ Error al cargar detalles: {character_detail['error']}")

    else:
        st.info("ℹ️ No hay personajes disponibles para editar o eliminar.")

st.markdown("---")
st.caption(
    "💡 Tip: Asegúrate de que la API Flask esté corriendo en http://localhost:5000"
)
