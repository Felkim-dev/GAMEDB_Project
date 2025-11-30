import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Agregar el directorio parent al path para importar el api_client
sys.path.append(str(Path(__file__).parent.parent))

from components.api_client import APIClient

# Configuración de la página
st.set_page_config(page_title="Items", page_icon="⚔️", layout="wide")

# Inicializar cliente API
api = APIClient()

st.title("⚔️ Gestión de Items")
st.markdown("---")

Item_types = {'Arma':0,'Armadura':1,'Comestible':2,'Coleccionables':3}
Item_rarity = {'Common':0,'Special':1,'Epic':2,'Legendary':3}


# Tabs para diferentes acciones
tab1, tab2, tab3 = st.tabs(
    ["📋 Ver Items", "➕ Crear Items", "✏️ Editar/Eliminar"]
)

# ==================== TAB 1: VER JUGADORES ====================
with tab1:
    st.header("Lista de Items")

    if st.button("🔄 Actualizar Lista", key="refresh_items"):
        st.rerun()

    items = api.get_items()

    if "error" in items:
        st.error(f"❌ Error al cargar lositems: {items['error']}")
    elif not items["items"]:
        st.info("ℹ️ No hay items registrados todavía.")
    else:

        df = pd.DataFrame(items["items"])
        # Cambia este orden según tu preferencia
        column_order = ["ItemID", "Name", "Type", "Rarity"]
        df = df[column_order]

        # Mostrar items en formato de tabla
        st.dataframe(
            df,
            width="stretch",
            hide_index=True,
        )

        st.success(f"✅ Total de items: {len(items['items'])}")

# ==================== TAB 2: CREAR JUGADOR ====================
with tab2:
    st.header("Crear Nuevo Item")

    with st.form("create_item_form"):
        col1, col2, col3= st.columns(3)

        with col1:
            item_name = st.text_input("Nombre de Item*", placeholder="Item123")

        with col2:
            selected_Type = st.selectbox(
                "Selecciona el tipo de Item:",
                options=list(Item_types.keys()),
                )

        with col3:
            selected_Rarity = st.selectbox(
                "Selecciona la rareza:",
                options=list(Item_rarity.keys()),
            )
            
        submitted = st.form_submit_button("➕ Crear Item", width="stretch")

        if submitted:
            if not item_name :
                st.error("❌ Todos los campos marcados con * son obligatorios")
            else:
                # Preparar datos
                item_data = {
                    "Name": item_name,
                    "Type": selected_Type,
                    "Rarity": selected_Rarity,
                }

                
                # Llamar a la API
                result = api.create_item(item_data)
                if "error" in result:
                    st.error(f"❌ Error: {result['error']}")
                else:
                    st.success("✅ Item creado exitosamente!")
                    st.balloons()
                    st.json(result)

# ==================== TAB 3: EDITAR/ELIMINAR ====================
with tab3:
    st.header("Editar o Eliminar Item")

    items = api.get_items()

    if "error" not in items and items["items"]:

        # Selector de jugador
        items_options = {
            f"{p['ItemID']} - {p['Name']}": p["ItemID"]
            for p in items["items"]
        }
        selected_item = st.selectbox(
            "Selecciona un item:", options=list(items_options.keys())
        )

        if selected_item:
            item_id = items_options[selected_item]
            item_detail = api.get_item(item_id)

            if "error" not in item_detail:
                col1, col2 = st.columns(2)

                # Columna 1: Editar
                with col1:
                    st.subheader("✏️ Editar Item")

                    with st.form("edit_item_form"):
                        new_name = st.text_input(
                            "Nombre de Item", value=item_detail.get("Name", "")
                        )
                        new_type = st.selectbox(
                            "Selecciona el tipo de Item:",
                            options=Item_types,
                        )
                        
                        new_Rarity = st.selectbox(
                            "Selecciona la rareza:",
                            options=Item_rarity,
                        )
                        update_submitted = st.form_submit_button(
                            "💾 Actualizar", width="stretch"
                        )

                        if update_submitted:
                            updated_data = {
                                "Name": new_name,
                                "Type": new_type,
                                "Rarity": new_Rarity,
                            }

                            result = api.update_item(item_id, updated_data)

                            if "error" in result:
                                st.error(f"❌ Error: {result['error']}")
                            else:
                                st.success("✅ Item actualizado exitosamente!")
                                st.rerun()

                # Columna 2: Eliminar
                with col2:
                    st.subheader("🗑️ Eliminar Item")
                    st.warning(
                        "⚠️ Esta acción no se puede deshacer"
                    )

                    confirm = st.checkbox("Confirmo que quiero eliminar este item")

                    if st.button(
                        "🗑️ Eliminar Item",
                        disabled=not confirm,
                        width="stretch",
                    ):
                        result = api.delete_item(item_id)

                        if "error" in result:
                            st.error(f"❌ Error: {result['error']}")
                        else:
                            st.success("✅ Item eliminado exitosamente!")
                            st.rerun()
            else:
                st.error(f"❌ Error al cargar detalles: {item_detail['error']}")
    else:
        st.info("ℹ️ No hay items disponibles para editar o eliminar.")

st.markdown("---")
st.caption(
    "💡 Tip: Asegúrate de que la API Flask esté corriendo en http://localhost:5000"
)
