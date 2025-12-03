import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Agregar el directorio parent al path para importar el api_client
sys.path.append(str(Path(__file__).parent.parent))

from components.api_client import APIClient

# Configuración de la página
st.set_page_config(page_title="Reportes", page_icon="📊", layout="wide")

# Inicializar cliente API
api = APIClient()

st.title("📊 Reportes y Análisis (JOINs)")
st.markdown("---")

# Obtener lista de reportes disponibles
available_reports = api.get_available_reports()

if "error" in available_reports:
    st.error(f"❌ Error al cargar reportes: {available_reports['error']}")
else:
    # Selector de reporte
    report_options = {
        f"{r['id']}. {r['name']}": r["id"]
        for r in available_reports.get("available_reports", [])
    }

    selected_report = st.selectbox(
        "Selecciona un reporte:", options=list(report_options.keys())
    )

    st.markdown("---")

    # Botón para generar reporte
    if st.button("📈 Generar Reporte", use_container_width=True, type="primary"):
        report_id = report_options[selected_report]

        with st.spinner("Generando reporte..."):

            # ==================== REPORTE 1: Personajes con Jugadores ====================
            if report_id == 1:
                st.subheader("🦸 Personajes con sus Jugadores")
                st.caption("JOIN: Character ⟕ Player")

                data = api.get_characters_with_players()

                if "error" in data:
                    st.error(f"❌ Error: {data['error']}")
                elif not data.get("report"):
                    st.info("ℹ️ No hay datos disponibles")
                else:
                    df = pd.DataFrame(data["report"])
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    st.success(f"✅ Total de registros: {len(data['report'])}")

                    # Estadística adicional
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total de Personajes", len(data["report"]))
                    with col2:
                        unique_players = df["PlayerID"].nunique()
                        st.metric("Jugadores Únicos", unique_players)

            # ==================== REPORTE 2: Inventario Detallado ====================
            elif report_id == 2:
                st.subheader("🎒 Inventario Detallado")
                st.caption("JOIN: Inventory ⟕ Character ⟕ Item ⟕ Player")

                data = api.get_inventory_details()

                if "error" in data:
                    st.error(f"❌ Error: {data['error']}")
                elif not data.get("report"):
                    st.info("ℹ️ No hay datos disponibles")
                else:
                    df = pd.DataFrame(data["report"])
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    st.success(f"✅ Total de registros: {len(data['report'])}")

                    # Gráfico de rareza
                    st.markdown("### 📊 Distribución por Rareza")
                    rarity_count = df["ItemRarity"].value_counts()
                    st.bar_chart(rarity_count)

                    # Tabla de resumen por tipo
                    st.markdown("### 📋 Resumen por Tipo de Item")
                    type_summary = (
                        df.groupby("ItemType")["Quantity"].sum().reset_index()
                    )
                    st.dataframe(
                        type_summary, use_container_width=True, hide_index=True
                    )

            # ==================== REPORTE 3: Progreso de Misiones ====================
            elif report_id == 3:
                st.subheader("🎯 Progreso de Misiones")
                st.caption("JOIN: CharacterMission ⟕ Character ⟕ Mission ⟕ Player")

                data = api.get_missions_progress()

                if "error" in data:
                    st.error(f"❌ Error: {data['error']}")
                elif not data.get("report"):
                    st.info("ℹ️ No hay datos disponibles")
                else:
                    df = pd.DataFrame(data["report"])
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    st.success(f"✅ Total de registros: {len(data['report'])}")

                    # Métricas
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        complete = len(df[df["Status"] == "Complete"])
                        st.metric("✅ Completadas", complete)
                    with col2:
                        in_progress = len(df[df["Status"] == "In Progress"])
                        st.metric("🔄 En Progreso", in_progress)
                    with col3:
                        incomplete = len(df[df["Status"] == "Incomplete"])
                        st.metric("⏸️ Incompletas", incomplete)

                    # Gráfico de estado
                    st.markdown("### 📊 Estado de las Misiones")
                    status_count = df["Status"].value_counts()
                    st.bar_chart(status_count)

            # ==================== REPORTE 4: Detalles de Transacciones ====================
            elif report_id == 4:
                st.subheader("💱 Detalles de Transacciones")
                st.caption(
                    "JOIN: Transaction ⟕ Character (Giver) ⟕ Character (Receiver) ⟕ Item"
                )

                data = api.get_transactions_details()

                if "error" in data:
                    st.error(f"❌ Error: {data['error']}")
                elif not data.get("report"):
                    st.info("ℹ️ No hay datos disponibles")
                else:
                    df = pd.DataFrame(data["report"])
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    st.success(f"✅ Total de registros: {len(data['report'])}")

                    # Gráfico por tipo de transacción
                    st.markdown("### 📊 Transacciones por Tipo")
                    type_count = df["TransactionType"].value_counts()
                    st.bar_chart(type_count)

            # ==================== REPORTE 5: Estadísticas por Jugador ====================
            elif report_id == 5:
                st.subheader("📈 Estadísticas por Jugador")
                st.caption("JOIN con GROUP BY y funciones de agregación")

                data = api.get_player_statistics()

                if "error" in data:
                    st.error(f"❌ Error: {data['error']}")
                elif not data.get("report"):
                    st.info("ℹ️ No hay datos disponibles")
                else:
                    df = pd.DataFrame(data["report"])
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    st.success(f"✅ Total de jugadores: {len(data['report'])}")

                    # Jugador con más personajes
                    top_player = df.loc[df["TotalCharacters"].idxmax()]
                    st.markdown(
                        f"### 🏆 Jugador con más personajes: **{top_player['UserName']}** ({top_player['TotalCharacters']} personajes)"
                    )

                    # Gráfico de personajes por jugador
                    st.markdown("### 📊 Personajes por Jugador")
                    chart_data = df[["UserName", "TotalCharacters"]].set_index(
                        "UserName"
                    )
                    st.bar_chart(chart_data)

            # ==================== REPORTE 6: Perfil de Personaje ====================
            elif report_id == 6:
                st.subheader("👤 Perfil Completo de Personaje")
                st.caption("Múltiples JOINs para información detallada")

                # Obtener lista de personajes
                characters = api.get_characters()

                if "error" not in characters and characters.get("characters"):
                    char_options = {
                        f"{c['CharacterID']} - {c['Name']}": c["CharacterID"]
                        for c in characters["characters"]
                    }

                    selected_char = st.selectbox(
                        "Selecciona un personaje:", options=list(char_options.keys())
                    )

                    if st.button("🔍 Ver Perfil", use_container_width=True):
                        char_id = char_options[selected_char]
                        data = api.get_character_profile(char_id)

                        if "error" in data:
                            st.error(f"❌ Error: {data['error']}")
                        else:
                            profile = data["profile"]

                            # Información básica
                            st.markdown("### 📋 Información Básica")
                            info = profile["character_info"]
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Nivel", info["Level"])
                            with col2:
                                st.metric("Experiencia", info["Experience"])
                            with col3:
                                st.write(f"**Jugador:** {info['PlayerName']}")
                            with col4:
                                st.write(f"**Email:** {info['PlayerEmail']}")

                            # Inventario
                            st.markdown("### 🎒 Inventario")
                            if profile["inventory"]:
                                inv_df = pd.DataFrame(profile["inventory"])
                                st.dataframe(
                                    inv_df, use_container_width=True, hide_index=True
                                )
                            else:
                                st.info("Sin items en el inventario")

                            # Misiones
                            st.markdown("### 🎯 Misiones")
                            if profile["missions"]:
                                miss_df = pd.DataFrame(profile["missions"])
                                st.dataframe(
                                    miss_df, use_container_width=True, hide_index=True
                                )
                            else:
                                st.info("Sin misiones asignadas")

                            # Transacciones
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("### 📤 Items Dados")
                                if profile["transactions_given"]:
                                    given_df = pd.DataFrame(
                                        profile["transactions_given"]
                                    )
                                    st.dataframe(
                                        given_df,
                                        use_container_width=True,
                                        hide_index=True,
                                    )
                                else:
                                    st.info("Sin transacciones salientes")

                            with col2:
                                st.markdown("### 📥 Items Recibidos")
                                if profile["transactions_received"]:
                                    rec_df = pd.DataFrame(
                                        profile["transactions_received"]
                                    )
                                    st.dataframe(
                                        rec_df,
                                        use_container_width=True,
                                        hide_index=True,
                                    )
                                else:
                                    st.info("Sin transacciones entrantes")
                else:
                    st.info("ℹ️ No hay personajes disponibles")

            # ==================== REPORTE 7: Distribución de Items ====================
            elif report_id == 7:
                st.subheader("📦 Distribución de Items")
                st.caption("JOIN con GROUP BY: Items por tipo y cantidad")

                data = api.get_items_distribution()

                if "error" in data:
                    st.error(f"❌ Error: {data['error']}")
                elif not data.get("report"):
                    st.info("ℹ️ No hay datos disponibles")
                else:
                    df = pd.DataFrame(data["report"])
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    st.success(f"✅ Total de items: {len(data['report'])}")

                    # Métricas
                    col1, col2 = st.columns(2)
                    with col1:
                        total_quantity = df["TotalQuantity"].sum()
                        st.metric("Items Totales en el Juego", total_quantity)
                    with col2:
                        total_owners = df["TotalOwners"].sum()
                        st.metric("Total de Propietarios", total_owners)

                    # Gráficos
                    st.markdown("### 📊 Items por Tipo")
                    type_qty = df.groupby("Type")["TotalQuantity"].sum()
                    st.bar_chart(type_qty)

                    st.markdown("### 💎 Items por Rareza")
                    rarity_qty = df.groupby("Rarity")["TotalQuantity"].sum()
                    st.bar_chart(rarity_qty)

st.markdown("---")
st.caption(
    "💡 Tip: Estos reportes utilizan JOINs de SQL para combinar información de múltiples tablas"
)
