import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Agregar el directorio parent al path para importar el api_client
sys.path.append(str(Path(__file__).parent.parent))

from components.api_client import APIClient

# Configuración de la página
st.set_page_config(page_title="Inventario", page_icon="🎒", layout="wide")

# Inicializar cliente API
api = APIClient()

st.title("🎒 Gestión de Inventario")
st.markdown("---")

characters = api.get_characters()
items = api.get_items()

if (
    "error" not in characters
    and characters.get("characters")
    and "error" not in items
    and items.get("items")
):

    # Tabs para diferentes acciones
    tab1, tab2, tab3 = st.tabs(
        ["📋 Ver Inventarios", "➕ Crear Inventario", "✏️ Editar/Eliminar"]
    )

    # ==================== TAB 1: VER INVENTARIOS ====================
    with tab1:
        st.header("Lista de Inventarios")

        if st.button("🔄 Actualizar Lista", key="refresh_inventories"):
            st.rerun()

        inventories = api.get_inventories()
        print(inventories)
        
        if "error" in inventories:
            st.error(f"❌ Error al cargar los inventarios: {inventories['error']}")
        elif not inventories.get("inventory"):
            st.info("ℹ️ No hay inventarios registrados todavía.")
        else:
            df = pd.DataFrame(inventories["inventory"])
            # Ordenar columnas
            column_order = ["CharacterID", "ItemID", "Quantity"]
            df = df[column_order]

            # Mostrar en formato de tabla
            st.dataframe(
                df,
                width='stretch',
                hide_index=True,
            )

            st.success(f"✅ Total de inventarios: {len(inventories['inventory'])}")

    # ==================== TAB 2: CREAR INVENTARIO ====================
    with tab2:

        st.header("Crear Nuevo Inventario")

        with st.form("create_inventory_form"):

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

            # Crear opciones para items con formato ID - Nombre
            item_options = {
                f"{i['ItemID']} - {i['Name']}": i["ItemID"] for i in items["items"]
            }

            with col2:
                selected_item_key = st.selectbox(
                    "Selecciona el item:",
                    options=list(item_options.keys()),
                )
                selected_item = item_options[selected_item_key]

            quantity = st.number_input(
                "Cantidad*",
                min_value=1,
                max_value=9999,
                value=1,
                help="Cantidad del item en el inventario",
            )

            # Botón de submit
            submitted = st.form_submit_button(
                "➕ Crear Inventario", width='stretch'
            )

            if submitted:
                # Preparar datos
                inventory_data = {
                    "CharacterID": selected_character,
                    "ItemID": selected_item,
                    "Quantity": quantity,
                }

                # Llamar a la API
                result = api.create_inventory(inventory_data)
                if "error" in result:
                    st.error(f"❌ Error: {result['error']}")
                else:
                    st.success("✅ Inventario creado exitosamente!")
                    st.balloons()
                    st.json(result)

    # ==================== TAB 3: EDITAR/ELIMINAR ====================
    with tab3:
        st.header("Editar o Eliminar Inventario")

        inventories = api.get_inventories()

        if "error" not in inventories and inventories.get("inventory"):

            # Selector de inventario
            inventory_options = {
                f"Character ID: {inv['CharacterID']} - Item ID: {inv['ItemID']} (Qty: {inv['Quantity']})": (
                    inv["CharacterID"],
                    inv["ItemID"],
                )
                for inv in inventories["inventory"]
            }
            selected_inventory = st.selectbox(
                "Selecciona un inventario:", options=list(inventory_options.keys())
            )

            if selected_inventory:
                character_id, item_id = inventory_options[selected_inventory]
                inventory_detail = api.get_inventory(character_id, item_id)

                if "error" not in inventory_detail:
                    col1, col2 = st.columns(2)

                    # Columna 1: Editar
                    with col1:
                        st.subheader("✏️ Editar Inventario")

                        with st.form("edit_inventory_form"):
                            new_quantity = st.number_input(
                                "Cantidad:",
                                min_value=1,
                                max_value=9999,
                                value=inventory_detail.get("Quantity", 1),
                            )

                            update_submitted = st.form_submit_button(
                                "💾 Actualizar", width='stretch'
                            )

                            if update_submitted:
                                updated_data = {
                                    "Quantity": new_quantity,
                                }

                                result = api.update_inventory(
                                    character_id, item_id, updated_data
                                )

                                if "error" in result:
                                    st.error(f"❌ Error: {result['error']}")
                                else:
                                    st.success(
                                        "✅ Inventario actualizado exitosamente!"
                                    )
                                    st.rerun()

                    # Columna 2: Eliminar
                    with col2:
                        st.subheader("🗑️ Eliminar Inventario")
                        st.warning("⚠️ Esta acción no se puede deshacer")

                        confirm = st.checkbox(
                            "Confirmo que quiero eliminar este inventario"
                        )

                        if st.button(
                            "🗑️ Eliminar Inventario",
                            disabled=not confirm,
                            width='stretch',
                        ):
                            result = api.delete_inventory(character_id, item_id)

                            if "error" in result:
                                st.error(f"❌ Error: {result['error']}")
                            else:
                                st.success("✅ Inventario eliminado exitosamente!")
                                st.rerun()
                else:
                    st.error(
                        f"❌ Error al cargar detalles: {inventory_detail['error']}"
                    )
        else:
            st.info("ℹ️ No hay inventarios disponibles para editar o eliminar.")

else:
    st.info("ℹ️ Necesitas tener personajes e items creados para gestionar inventarios.")

st.markdown("---")
st.caption(
    "💡 Tip: Asegúrate de que la API Flask esté corriendo en http://localhost:5000"
)
