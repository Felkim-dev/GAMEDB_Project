import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Agregar el directorio parent al path para importar el api_client
sys.path.append(str(Path(__file__).parent.parent))

from components.api_client import APIClient

# Configuración de la página
st.set_page_config(page_title="Transacciones", page_icon="💱", layout="wide")

# Inicializar cliente API
api = APIClient()

st.title("💱 Gestión de Transacciones")
st.markdown("---")

Transaction_Type = ["Trade", "Purchase", "Donation"]

characters = api.get_characters()
item = api.get_items()

if len(characters["characters"]) >= 2:

    # Tabs para diferentes acciones
    tab1, tab2, tab3 = st.tabs(
        ["📋 Ver Transacciones", "➕ Crear Transacciones", "✏️ Editar/Eliminar"]
    )

    # ==================== TAB 1: VER JUGADORES ====================
    with tab1:
        st.header("Lista de Transacciones")

        if st.button("🔄 Actualizar Lista", key="refresh_transactions"):
            st.rerun()

        transactions = api.get_transactions()

        if "error" in transactions:
            st.error(f"❌ Error al cargar las trasnsacciones: {transactions['error']}")
        elif not transactions["transactions"]:
            st.info("ℹ️ No hay transacciones registradas todavía.")
        else:

            df = pd.DataFrame(transactions["transactions"])
            # Cambia este orden según tu preferencia
            column_order = [
                "TransactionID",
                "GiverID",
                "ReceiverID",
                "TransactionType",
                "ItemID",
                "TransactionDate",
            ]
            df = df[column_order]

            # Mostrar items en formato de tabla
            st.dataframe(
                df,
                width="stretch",
                hide_index=True,
            )

            st.success(
                f"✅ Total de transacciones: {len(transactions['transactions'])}"
            )

    # ==================== TAB 2: CREAR JUGADOR ====================
    with tab2:

        st.header("Crear Nuevas Transacciones")

        with st.form("create_transaction_form"):

            col1, col2 = st.columns(2)

            # Crear opciones para personajes con formato ID - Nombre
            character_options = {
                f"{char['CharacterID']} - {char['Name']}": char["CharacterID"]
                for char in characters["characters"]
            }

            with col1:
                selected_giver_key = st.selectbox(
                    "Selecciona el personaje dador:",
                    options=list(character_options.keys()),
                )
                selected_giver = character_options[selected_giver_key]

            # Filtrar personajes excluyendo el dador
            receiver_options = {
                k: v for k, v in character_options.items() if v != selected_giver
            }

            with col2:
                selected_receiver_key = st.selectbox(
                    "Selecciona el personaje recibidor:",
                    options=list(receiver_options.keys()),
                )
                selected_receiver = receiver_options[selected_receiver_key]

            col3, col4 = st.columns(2)

            # Crear opciones para items con formato ID - Nombre
            item_options = {
                f"{i['ItemID']} - {i['Name']}": i["ItemID"] for i in item["items"]
            }

            with col3:
                transaction_type = st.selectbox(
                    "Seleccion de tipo de transacción:",
                    options=Transaction_Type,
                )

            with col4:
                transaction_date = st.date_input(
                    "Fecha de Transacción*",
                    help="Fecha en que se realizó la transacción",
                )

            item_select_key = st.selectbox(
                "Selecciona el item:",
                options=list(item_options.keys()),
            )

            item_select = item_options[item_select_key]

            # Botón de submit fuera de las columnas
            submitted = st.form_submit_button(
                "➕ Crear transaccion", use_container_width=True
            )

            if submitted:
                # Preparar datos
                transacction_data = {
                    "ItemID": item_select,
                    "GiverID": selected_giver,
                    "ReceiverID": selected_receiver,
                    "TransactionDate": str(transaction_date),
                    "TransactionType": transaction_type,
                }

                print(transacction_data)

                # Llamar a la API
                result = api.create_transaction(transacction_data)
                if "error" in result:
                    st.error(f"❌ Error: {result['error']}")
                else:
                    st.success("✅ Transacción creado exitosamente!")
                    st.balloons()
                    st.json(result)

    # ==================== TAB 3: EDITAR/ELIMINAR ====================
    with tab3:
        st.header("Editar o Eliminar Transaccion")

        transactions = api.get_transactions()

        if "error" not in transactions and transactions["transactions"]:

            # Selector de jugador
            transactions_options = {
                f"ID: {p['TransactionID']} --> Giver: {p['GiverID']} to Receiver:{p['ReceiverID']}": p[
                    "TransactionID"
                ]
                for p in transactions["transactions"]
            }
            selected_transaction = st.selectbox(
                "Selecciona una transaccion:", options=list(transactions_options.keys())
            )

            if selected_transaction:
                transaction_id = transactions_options[selected_transaction]
                transaction_detail = api.get_transaction(transaction_id)

                if "error" not in transaction_detail:
                    col1, col2 = st.columns(2)

                    # Columna 1: Editar
                    with col1:
                        st.subheader("✏️ Editar Transacción")

                        with st.form("edit_transaction_form"):
                            # Crear opciones para items
                            item_options_edit = {
                                f"{i['ItemID']} - {i['Name']}": i["ItemID"]
                                for i in item["items"]
                            }

                            # Selector de Item con valor actual
                            current_item_key = next(
                                (
                                    k
                                    for k, v in item_options_edit.items()
                                    if v == transaction_detail.get("ItemID")
                                ),
                                list(item_options_edit.keys())[0],
                            )

                            new_item_key = st.selectbox(
                                "Item:",
                                options=list(item_options_edit.keys()),
                                index=list(item_options_edit.keys()).index(
                                    current_item_key
                                ),
                            )
                            new_item = item_options_edit[new_item_key]

                            # Selector de tipo
                            new_type = st.selectbox(
                                "Tipo de Transacción:",
                                options=Transaction_Type,
                                index=Transaction_Type.index(
                                    transaction_detail.get("TransactionType", "Trade")
                                ),
                            )

                            # Selector de fecha
                            new_date = st.date_input("Fecha de Transacción:")

                            update_submitted = st.form_submit_button(
                                "💾 Actualizar", use_container_width=True
                            )

                            if update_submitted:
                                updated_data = {
                                    "ItemID": new_item,
                                    "TransactionType": new_type,
                                    "TransactionDate": str(new_date),
                                }

                                result = api.update_transaction(
                                    transaction_id, updated_data
                                )

                                if "error" in result:
                                    st.error(f"❌ Error: {result['error']}")
                                else:
                                    st.success(
                                        "✅ Transacción actualizada exitosamente!"
                                    )
                                    st.rerun()

                    # Columna 2: Eliminar
                    with col2:
                        st.subheader("🗑️ Eliminar Transacción")
                        st.warning("⚠️ Esta acción no se puede deshacer")

                        confirm = st.checkbox(
                            "Confirmo que quiero eliminar esta transacción"
                        )

                        if st.button(
                            "🗑️ Eliminar Transacción",
                            disabled=not confirm,
                            use_container_width=True,
                        ):
                            result = api.delete_transaction(transaction_id)

                            if "error" in result:
                                st.error(f"❌ Error: {result['error']}")
                            else:
                                st.success("✅ Transacción eliminada exitosamente!")
                                st.rerun()
                else:
                    st.error(
                        f"❌ Error al cargar detalles: {transaction_detail['error']}"
                    )
        else:
            st.info("ℹ️ No hay transacciones disponibles para editar o eliminar.")

else:
    st.info("ℹ️ No existen jugadores suficientes para mostrar o hacer transacciones.")

st.markdown("---")
st.caption(
    "💡 Tip: Asegúrate de que la API Flask esté corriendo en http://localhost:5000"
)
