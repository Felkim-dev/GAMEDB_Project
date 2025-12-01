import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Agregar el directorio parent al path para importar el api_client
sys.path.append(str(Path(__file__).parent.parent))

from components.api_client import APIClient

# Configuración de la página
st.set_page_config(page_title="Asignación de Misiones", page_icon="🎯", layout="wide")

# Inicializar cliente API
api = APIClient()

st.title("🎯 Asignación de Misiones a Personajes")
st.markdown("---")

Mission_Status = ["Incomplete", "In Progress", "Complete"]

characters = api.get_characters()
missions = api.get_missions()

if (
    "error" not in characters
    and characters.get("characters")
    and "error" not in missions
    and missions.get("missions")
):

    # Tabs para diferentes acciones
    tab1, tab2, tab3 = st.tabs(
        ["📋 Ver Asignaciones", "➕ Asignar Misión", "✏️ Editar/Eliminar"]
    )

    # ==================== TAB 1: VER ASIGNACIONES ====================
    with tab1:
        st.header("Lista de Misiones Asignadas")

        if st.button("🔄 Actualizar Lista", key="refresh_character_missions"):
            st.rerun()

        character_missions = api.get_character_missions()

        if "error" in character_missions:
            st.error(
                f"❌ Error al cargar las asignaciones: {character_missions['error']}"
            )
        elif not character_missions.get("character_missions"):
            st.info("ℹ️ No hay misiones asignadas todavía.")
        else:
            df = pd.DataFrame(character_missions["character_missions"])
            # Ordenar columnas
            column_order = [
                "CharacterID",
                "MissionID",
                "Status",
                "StartDate",
                "CompletionDate",
            ]
            df = df[column_order]

            # Mostrar en formato de tabla
            st.dataframe(
                df,
                width='stretch',
                hide_index=True,
            )

            st.success(
                f"✅ Total de asignaciones: {len(character_missions['character_missions'])}"
            )

    # ==================== TAB 2: ASIGNAR MISIÓN ====================
    with tab2:

        st.header("Asignar Misión a Personaje")

        with st.form("create_character_mission_form"):

            col1, col2 = st.columns(2)

            # Crear opciones para personajes con formato ID - Nombre
            character_options = {
                f"{char['CharacterID']} - {char['Name']}": char["CharacterID"]
                for char in characters["characters"]
            }

            with col1:
                selected_character_key = st.selectbox(
                    "Selecciona el personaje:",
                    options=list(character_options.keys()),
                )
                selected_character = character_options[selected_character_key]

            # Crear opciones para misiones con formato ID - Nombre
            mission_options = {
                f"{m['MissionID']} - {m['Title']}": m["MissionID"]
                for m in missions["missions"]
            }

            with col2:
                selected_mission_key = st.selectbox(
                    "Selecciona la misión:",
                    options=list(mission_options.keys()),
                )
                selected_mission = mission_options[selected_mission_key]

            col3, col4, col5 = st.columns(3)

            with col3:
                status = st.selectbox(
                    "Estado de la misión:",
                    options=Mission_Status,
                )

            with col4:
                start_date = st.date_input(
                    "Fecha de Inicio*",
                    help="Fecha en que se inició la misión",
                )

            with col5:
                completion_date = st.date_input(
                    "Fecha de Finalización",
                    help="Fecha en que se completó la misión (opcional)",
                    value=None,
                )

            # Botón de submit
            submitted = st.form_submit_button(
                "➕ Asignar Misión", width='stretch'
            )

            if submitted:
                # Preparar datos
                character_mission_data = {
                    "CharacterID": selected_character,
                    "MissionID": selected_mission,
                    "Status": status,
                    "StartDate": str(start_date),
                }

                # Agregar fecha de finalización solo si fue proporcionada
                if completion_date:
                    character_mission_data["CompletionDate"] = str(completion_date)

                # Llamar a la API
                result = api.create_character_mission(character_mission_data)
                if "error" in result:
                    st.error(f"❌ Error: {result['error']}")
                else:
                    st.success("✅ Misión asignada exitosamente!")
                    st.balloons()
                    st.json(result)

    # ==================== TAB 3: EDITAR/ELIMINAR ====================
    with tab3:
        st.header("Editar o Eliminar Asignación")

        character_missions = api.get_character_missions()

        if "error" not in character_missions and character_missions.get(
            "character_missions"
        ):

            # Selector de asignación
            cm_options = {
                f"Character ID: {cm['CharacterID']} - Mission ID: {cm['MissionID']} ({cm['Status']})": (
                    cm["CharacterID"],
                    cm["MissionID"],
                )
                for cm in character_missions["character_missions"]
            }
            selected_cm = st.selectbox(
                "Selecciona una asignación:", options=list(cm_options.keys())
            )

            if selected_cm:
                character_id, mission_id = cm_options[selected_cm]
                cm_detail = api.get_character_mission(character_id, mission_id)

                if "error" not in cm_detail:
                    col1, col2 = st.columns(2)

                    # Columna 1: Editar
                    with col1:
                        st.subheader("✏️ Editar Asignación")

                        with st.form("edit_character_mission_form"):
                            new_status = st.selectbox(
                                "Estado:",
                                options=Mission_Status,
                                index=Mission_Status.index(
                                    cm_detail.get("Status", "Incomplete")
                                ),
                            )

                            new_start_date = st.date_input("Fecha de Inicio:")

                            new_completion_date = st.date_input(
                                "Fecha de Finalización (opcional):",
                                value=None,
                            )

                            update_submitted = st.form_submit_button(
                                "💾 Actualizar", width='stretch'
                            )

                            if update_submitted:
                                updated_data = {
                                    "Status": new_status,
                                    "StartDate": str(new_start_date),
                                }

                                # Agregar fecha de finalización solo si fue proporcionada
                                if new_completion_date:
                                    updated_data["CompletionDate"] = str(
                                        new_completion_date
                                    )

                                result = api.update_character_mission(
                                    character_id, mission_id, updated_data
                                )

                                if "error" in result:
                                    st.error(f"❌ Error: {result['error']}")
                                else:
                                    st.success(
                                        "✅ Asignación actualizada exitosamente!"
                                    )
                                    st.rerun()

                    # Columna 2: Eliminar
                    with col2:
                        st.subheader("🗑️ Eliminar Asignación")
                        st.warning("⚠️ Esta acción no se puede deshacer")

                        confirm = st.checkbox(
                            "Confirmo que quiero eliminar esta asignación"
                        )

                        if st.button(
                            "🗑️ Eliminar Asignación",
                            disabled=not confirm,
                            width='stretch',
                        ):
                            result = api.delete_character_mission(
                                character_id, mission_id
                            )

                            if "error" in result:
                                st.error(f"❌ Error: {result['error']}")
                            else:
                                st.success("✅ Asignación eliminada exitosamente!")
                                st.rerun()
                else:
                    st.error(f"❌ Error al cargar detalles: {cm_detail['error']}")
        else:
            st.info("ℹ️ No hay asignaciones disponibles para editar o eliminar.")

else:
    st.info("ℹ️ Necesitas tener personajes y misiones creados para asignar misiones.")

st.markdown("---")
st.caption(
    "💡 Tip: Asegúrate de que la API Flask esté corriendo en http://localhost:5000"
)
