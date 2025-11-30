"""
Cliente API para conectar el frontend de Streamlit con la API Flask
"""

import requests
from typing import Dict, List, Optional


class APIClient:
    """Cliente para realizar peticiones HTTP a la API Flask"""

    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url

    def _make_request(
        self, method: str, endpoint: str, data: Optional[Dict] = None
    ) -> Dict:
        """Método genérico para hacer peticiones HTTP"""
        url = f"{self.base_url}/{endpoint}"

        try:
            if method == "GET":
                response = requests.get(url)
            elif method == "POST":
                response = requests.post(url, json=data)
            elif method == "PUT":
                response = requests.put(url, json=data)
            elif method == "DELETE":
                response = requests.delete(url)
            else:
                raise ValueError(f"Método HTTP no soportado: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.ConnectionError:
            return {
                "error": "No se pudo conectar con la API. Verifica que esté corriendo."
            }
        except requests.exceptions.HTTPError as e:
            return {"error": f"Error HTTP: {e}"}
        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}

    # ==================== PLAYERS ====================

    def get_players(self) -> List[Dict]:
        """Obtiene todos los jugadores"""
        return self._make_request("GET", "players/")

    def get_player(self, player_id: int) -> Dict:
        """Obtiene un jugador específico por ID"""
        return self._make_request("GET", f"players/{player_id}")

    def create_player(self, data: Dict) -> Dict:
        """Crea un nuevo jugador"""
        return self._make_request("POST", "players", data)

    def update_player(self, player_id: int, data: Dict) -> Dict:
        """Actualiza un jugador existente"""
        return self._make_request("PUT", f"players/{player_id}", data)

    def delete_player(self, player_id: int) -> Dict:
        """Elimina un jugador"""
        return self._make_request("DELETE", f"players/{player_id}")

    # ==================== CHARACTERS ====================

    def get_characters(self) -> List[Dict]:
        """Obtiene todos los personajes"""
        return self._make_request("GET", "characters/")

    def get_character(self, character_id: int) -> Dict:
        """Obtiene un personaje específico por ID"""
        return self._make_request("GET", f"characters/{character_id}")

    def create_character(self, data: Dict) -> Dict:
        """Crea un nuevo personaje"""
        return self._make_request("POST", "characters", data)

    def update_character(self, character_id: int, data: Dict) -> Dict:
        """Actualiza un personaje existente"""
        return self._make_request("PUT", f"characters/{character_id}", data)

    def delete_character(self, character_id: int) -> Dict:
        """Elimina un personaje"""
        return self._make_request("DELETE", f"characters/{character_id}")

    # ==================== ITEMS ====================

    def get_items(self) -> List[Dict]:
        """Obtiene todos los items"""
        return self._make_request("GET", "items")

    def get_item(self, item_id: int) -> Dict:
        """Obtiene un item específico por ID"""
        return self._make_request("GET", f"items/{item_id}")

    def create_item(self, data: Dict) -> Dict:
        """Crea un nuevo item"""
        return self._make_request("POST", "items", data)

    def update_item(self, item_id: int, data: Dict) -> Dict:
        """Actualiza un item existente"""
        return self._make_request("PUT", f"items/{item_id}", data)

    def delete_item(self, item_id: int) -> Dict:
        """Elimina un item"""
        return self._make_request("DELETE", f"items/{item_id}")

    # ==================== MISSIONS ====================

    def get_missions(self) -> List[Dict]:
        """Obtiene todas las misiones"""
        return self._make_request("GET", "missions")

    def get_mission(self, mission_id: int) -> Dict:
        """Obtiene una misión específica por ID"""
        return self._make_request("GET", f"missions/{mission_id}")

    def create_mission(self, data: Dict) -> Dict:
        """Crea una nueva misión"""
        return self._make_request("POST", "missions", data)

    def update_mission(self, mission_id: int, data: Dict) -> Dict:
        """Actualiza una misión existente"""
        return self._make_request("PUT", f"missions/{mission_id}", data)

    def delete_mission(self, mission_id: int) -> Dict:
        """Elimina una misión"""
        return self._make_request("DELETE", f"missions/{mission_id}")

    # ==================== HEALTH CHECK ====================

    def health_check(self) -> Dict:
        """Verifica el estado de la API"""
        try:
            response = requests.get(
                f"{self.base_url.replace('/api', '')}/health", timeout=2
            )
            return {"status": "ok" if response.status_code == 200 else "error"}
        except:
            return {"status": "offline"}
