# Frontend - Game Database Manager

Interfaz gráfica construida con Streamlit para gestionar la base de datos del juego.

## 📋 Requisitos Previos

1. Python 3.8 o superior
2. API Flask corriendo en `http://localhost:5000`
3. Base de datos MySQL corriendo (Docker container)

## 🚀 Instalación

### 1. Instalar dependencias

Desde la carpeta `frontend/`:

```cmd
pip install -r requirements.txt
```

## ▶️ Ejecutar la Aplicación

Desde la carpeta `frontend/`:

```cmd
streamlit run main.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📁 Estructura

```
frontend/
├── main.py                    # Página principal
├── pages/                     # Páginas de la aplicación
│   ├── 1_Players.py          # Gestión de jugadores
│   ├── 2_Characters.py       # Gestión de personajes (próximamente)
│   ├── 3_Items.py            # Gestión de items (próximamente)
│   ├── 4_Missions.py         # Gestión de misiones (próximamente)
│   └── 5_Transactions.py     # Gestión de transacciones (próximamente)
├── components/                # Componentes reutilizables
│   ├── __init__.py
│   └── api_client.py         # Cliente para comunicarse con la API
├── assets/                    # Recursos (imágenes, iconos)
└── requirements.txt           # Dependencias
```

## 🎯 Funcionalidades

### ✅ Implementadas:

- **Players**: Ver, crear, editar y eliminar jugadores

### 🔜 Por implementar:

- **Characters**: Gestión completa de personajes
- **Items**: Catálogo de items
- **Missions**: Sistema de misiones
- **Transactions**: Registro de transacciones

## 🔧 Configuración

Si tu API corre en un puerto diferente, edita `components/api_client.py`:

```python
api = APIClient(base_url="http://localhost:PUERTO/api")
```

## 📝 Notas

- Streamlit recarga automáticamente cuando guardas cambios en los archivos
- Usa el botón de actualizar (🔄) para refrescar los datos
- Los errores de conexión se mostrarán en pantalla si la API no está disponible

## 🐛 Solución de Problemas

### La aplicación no se conecta a la API

- Verifica que Flask esté corriendo: `http://localhost:5000`
- Revisa que no haya errores en la consola de Flask

### Error al instalar dependencias

```cmd
pip install --upgrade pip
pip install -r requirements.txt
```

### El navegador no se abre automáticamente

- Abre manualmente: `http://localhost:8501`
