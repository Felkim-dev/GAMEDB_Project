import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Agregar el directorio parent al path para importar el api_client
sys.path.append(str(Path(__file__).parent.parent))

from components.api_client import APIClient

# Configuración de la página
st.set_page_config(page_title="Mission", page_icon="🎯", layout="wide")

# Inicializar cliente API
api = APIClient()

st.title("🎯 Gestión de Misiones")
st.markdown("---")

dificultades = ["Easy", "Medium", "Hard"]

# Tabs para diferentes acciones
tab1, tab2, tab3 = st.tabs(
    ["📋 Ver Misiones", "➕ Crear Misiones", "✏️ Editar/Eliminar"]
)

# ==================== TAB 1: VER MISIONES ====================
with tab1:
    st.header("Lista de Misiones")

    if st.button("🔄 Actualizar Lista", key="refresh_missions"):
        st.rerun()

    missions = api.get_missions()

    if "error" in missions:
        st.error(f"❌ Error al cargar las misiones: {missions['error']}")
    elif not missions["missions"]:
        st.info("ℹ️ No hay misiones registrados todavía.")
    else:

        df = pd.DataFrame(missions["missions"])
        # Cambia este orden según tu preferencia
        column_order = ["MissionID", "Title", "Description", "Difficulty"]
        df = df[column_order]

        # Mostrar jugadores en formato de tabla
        st.dataframe(
            df,
            width="stretch",
            hide_index=True,
        )

        st.success(f"✅ Total de misiones: {len(missions['missions'])}")

# ==================== TAB 2: CREAR JUGADOR ====================
with tab2:
    st.header("Crear Nuevo Misiones")

    with st.form("create_mission_form"):
        col1, col2 = st.columns(2)

        with col1:
            title = st.text_input("Title*", placeholder="Title123", max_chars=100)

        with col2:
            selected_difficulty = st.selectbox(
                "Selecciona la dificultad:",
                options=dificultades,
            )

        Description = st.text_area(
            "Description*",
            placeholder="La mision trata sobre un caballero que...",
            height=150,
            max_chars=1000,
        )

        submitted = st.form_submit_button("➕ Crear Mision", width="stretch")

        if submitted:
            if not title or not Description:
                st.error("❌ Todos los campos marcados con * son obligatorios")
            else:
                # Preparar datos
                mission_data = {
                    "Title": title,
                    "Description": Description,
                    "Difficulty": selected_difficulty,
                }

                # Llamar a la API
                result = api.create_mission(mission_data)

                if "error" in result:
                    st.error(f"❌ Error: {result['error']}")
                else:
                    st.success("✅ Misión creada exitosamente!")
                    st.balloons()
                    st.json(result)

# ==================== TAB 3: EDITAR/ELIMINAR ====================
with tab3:
    st.header("Editar o Eliminar Misiones")

    missions = api.get_missions()

    if "error" not in missions and missions["missions"]:

        # Selector de jugador
        mission_options = {
            f"{p['MissionID']} - {p['Title']}": p["MissionID"]
            for p in missions["missions"]
        }
        selected_mission = st.selectbox(
            "Selecciona una mision:", options=list(mission_options.keys())
        )

        if selected_mission:
            mission_id = mission_options[selected_mission]
            mission_detail = api.get_mission(mission_id)

            if "error" not in mission_detail:
                col1, col2 = st.columns(2)

                # Columna 1: Editar
                with col1:
                    st.subheader("✏️ Editar Mision")

                    with st.form("edit_mision_form"):
                        new_title = st.text_input(
                            "Title",
                            value=mission_detail.get("Title", ""),
                            max_chars=100,
                        )
                        new_description = st.text_area(
                            "Description",
                            value=mission_detail.get("Description", ""),
                            height=150,
                            max_chars=1000,
                        )
                        new_difficulty = st.selectbox(
                            "Selecciona una dificultad:",
                            options=dificultades,
                        )

                        update_submitted = st.form_submit_button(
                            "💾 Actualizar", width="stretch"
                        )

                        if update_submitted:
                            updated_data = {
                                "Title": new_title,
                                "Description": new_description,
                                "Difficulty": new_difficulty,
                            }

                            result = api.update_mission(mission_id, updated_data)

                            if "error" in result:
                                st.error(f"❌ Error: {result['error']}")
                            else:
                                st.success("✅ Misión actualizada exitosamente!")
                                st.rerun()

                # Columna 2: Eliminar
                with col2:
                    st.subheader("🗑️ Eliminar Misión")
                    st.warning("⚠️ Esta acción no se puede deshacer.")

                    confirm = st.checkbox("Confirmo que quiero eliminar esta misión")

                    if st.button(
                        "🗑️ Eliminar Misión",
                        disabled=not confirm,
                        width="stretch",
                    ):
                        result = api.delete_mission(mission_id)

                        if "error" in result:
                            st.error(f"❌ Error: {result['error']}")
                        else:
                            st.success("✅ Misión eliminado exitosamente!")
                            st.rerun()
            else:
                st.error(f"❌ Error al cargar detalles: {mission_detail['error']}")
    else:
        st.info("ℹ️ No hay misiones disponibles para editar o eliminar.")

st.markdown("---")
st.caption(
    "💡 Tip: Asegúrate de que la API Flask esté corriendo en http://localhost:5000"
)
