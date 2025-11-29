import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Agregar el directorio parent al path para importar el api_client
sys.path.append(str(Path(__file__).parent.parent))

from components.api_client import APIClient

# Configuración de la página
st.set_page_config(page_title="Players", page_icon="👥", layout="wide")

# Inicializar cliente API
api = APIClient()

st.title("👥 Gestión de Jugadores")
st.markdown("---")

# Tabs para diferentes acciones
tab1, tab2, tab3 = st.tabs(
    ["📋 Ver Jugadores", "➕ Crear Jugador", "✏️ Editar/Eliminar"]
)

# ==================== TAB 1: VER JUGADORES ====================
with tab1:
    st.header("Lista de Jugadores")

    if st.button("🔄 Actualizar Lista", key="refresh_players"):
        st.rerun()

    players = api.get_players()

    print(players)

    if "error" in players:
        st.error(f"❌ Error al cargar jugadores: {players['error']}")
    elif not players:
        st.info("ℹ️ No hay jugadores registrados todavía.")
    else:
        
        df = pd.DataFrame(players["players"])
        # Cambia este orden según tu preferencia
        column_order = ["PlayerID", "UserName", "Email", "RegistrationDate"]
        df = df[column_order]

        # Mostrar jugadores en formato de tabla
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "PlayerID": st.column_config.NumberColumn(
                    "ID", help="ID único del jugador", width="small"
                ),
                "UserName": st.column_config.TextColumn(
                    "Usuario", help="Nombre de usuario", width="medium"
                ),
                "Email": st.column_config.TextColumn(
                    "Correo Electrónico", help="Email del jugador", width="medium"
                ),
                "RegistrationDate": st.column_config.DateColumn(
                    "Fecha de Registro",
                    help="Fecha en que se registró",
                    format="DD/MM/YYYY",
                    width="medium",
                ),
            },
        )

        st.success(f"✅ Total de jugadores: {len(players['players'])}")

# ==================== TAB 2: CREAR JUGADOR ====================
with tab2:
    st.header("Crear Nuevo Jugador")

    with st.form("create_player_form"):
        col1, col2 = st.columns(2)

        with col1:
            username = st.text_input("Nombre de Usuario*", placeholder="usuario123")

        with col2:
            email = st.text_input("Email*", placeholder="usuario@email.com")

        registration_date = st.date_input("Fecha de Registro*")

        submitted = st.form_submit_button("➕ Crear Jugador", use_container_width=True)

        if submitted:
            if not username or not email:
                st.error("❌ Todos los campos marcados con * son obligatorios")
            else:
                # Preparar datos
                player_data = {
                    "UserName": username,
                    "Email": email,
                    "RegistrationDate": str(registration_date),
                }

                # Llamar a la API
                result = api.create_player(player_data)

                if "error" in result:
                    st.error(f"❌ Error: {result['error']}")
                else:
                    st.success("✅ Jugador creado exitosamente!")
                    st.balloons()
                    st.json(result)

# ==================== TAB 3: EDITAR/ELIMINAR ====================
with tab3:
    st.header("Editar o Eliminar Jugador")

    players = api.get_players()

    if "error" not in players and players:
    
        # Selector de jugador
        player_options = {
            f"{p['PlayerID']} - {p['UserName']}": p["PlayerID"] for p in players["players"]
        }
        selected_player = st.selectbox(
            "Selecciona un jugador:", options=list(player_options.keys())
        )

        if selected_player:
            player_id = player_options[selected_player]
            player_detail = api.get_player(player_id)

            if "error" not in player_detail:
                col1, col2 = st.columns(2)

                # Columna 1: Editar
                with col1:
                    st.subheader("✏️ Editar Jugador")

                    with st.form("edit_player_form"):
                        new_username = st.text_input(
                            "Nombre de Usuario", value=player_detail.get("UserName", "")
                        )
                        new_email = st.text_input(
                            "Email", value=player_detail.get("Email", "")
                        )

                        update_submitted = st.form_submit_button(
                            "💾 Actualizar", use_container_width=True
                        )

                        if update_submitted:
                            updated_data = {
                                "UserName": new_username,
                                "Email": new_email,
                            }

                            result = api.update_player(player_id, updated_data)

                            if "error" in result:
                                st.error(f"❌ Error: {result['error']}")
                            else:
                                st.success("✅ Jugador actualizado exitosamente!")
                                st.rerun()

                # Columna 2: Eliminar
                with col2:
                    st.subheader("🗑️ Eliminar Jugador")
                    st.warning(
                        "⚠️ Esta acción no se puede deshacer y eliminará todos los personajes asociados."
                    )

                    confirm = st.checkbox("Confirmo que quiero eliminar este jugador")

                    if st.button(
                        "🗑️ Eliminar Jugador",
                        disabled=not confirm,
                        use_container_width=True,
                    ):
                        result = api.delete_player(player_id)

                        if "error" in result:
                            st.error(f"❌ Error: {result['error']}")
                        else:
                            st.success("✅ Jugador eliminado exitosamente!")
                            st.rerun()
            else:
                st.error(f"❌ Error al cargar detalles: {player_detail['error']}")
    else:
        st.info("ℹ️ No hay jugadores disponibles para editar o eliminar.")

st.markdown("---")
st.caption(
    "💡 Tip: Asegúrate de que la API Flask esté corriendo en http://localhost:5000"
)
