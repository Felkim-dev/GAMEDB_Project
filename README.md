# 🎮 Game Database Manager

Sistema completo de gestión de base de datos para videojuegos RPG, desarrollado con arquitectura de tres capas: MySQL, Flask REST API y Streamlit Frontend. Incluye operaciones CRUD completas, sistema de reportes con JOINs SQL avanzados y despliegue con Docker.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Modelo de Datos](#-modelo-de-datos)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Endpoints API](#-endpoints-api)
- [Reportes](#-reportes)
- [Estructura del Proyecto](#-estructura-del-proyecto)

## ✨ Características

### Funcionalidades Principales

- ✅ **CRUD Completo** para 7 entidades (Players, Characters, Items, Missions, Inventory, CharacterMission, Transactions)
- ✅ **REST API** con Flask y SQLAlchemy ORM
- ✅ **Interfaz Web Intuitiva** con Streamlit
- ✅ **7 Reportes Avanzados** utilizando JOINs SQL complejos
- ✅ **Validación de Datos** con Marshmallow schemas
- ✅ **Relaciones Many-to-Many** (Inventory, CharacterMission)
- ✅ **Sistema de Transacciones** entre personajes
- ✅ **Visualizaciones Interactivas** con pandas y gráficos
- ✅ **Docker Compose** para despliegue rápido
- ✅ **Persistencia de Datos** con volúmenes Docker

### Características Técnicas

- **Arquitectura de 3 Capas**: Separación clara entre datos, lógica y presentación
- **Relaciones CASCADE**: Integridad referencial automática
- **Foreign Keys**: Constraints para mantener consistencia
- **Healthchecks**: Verificación automática de servicios
- **Hot Reload**: Desarrollo ágil sin reiniciar contenedores
- **API RESTful**: Endpoints organizados por blueprints
- **Serialización**: Conversión automática JSON con Marshmallow

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────┐
│                  Frontend (Streamlit)               │
│                   Puerto 8501                       │
└────────────────────┬────────────────────────────────┘
                     │ HTTP Requests
                     ↓
┌─────────────────────────────────────────────────────┐
│              API REST (Flask)                       │
│                   Puerto 5000                       │
│  ┌──────────────────────────────────────────────┐  │
│  │ Routes → Services → Models → DB             │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────┘
                     │ SQLAlchemy ORM
                     ↓
┌─────────────────────────────────────────────────────┐
│         Base de Datos MySQL                         │
│                   Puerto 8080                       │
│  ┌──────────────────────────────────────────────┐  │
│  │ 7 Tablas Relacionales + Constraints          │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

## 🗄️ Modelo de Datos

### Esquema de Base de Datos

```sql
Player (Jugadores)
├── PlayerID (PK)
├── UserName
├── Email
└── RegistrationDate

Character (Personajes)
├── CharacterID (PK)
├── PlayerID (FK → Player)
├── Name
├── Level
└── Experience

Item (Objetos del juego)
├── ItemID (PK)
├── Name
├── Type (Arma, Armadura, Comestible, Coleccionables)
└── Rarity (Common, Special, Epic, Legendary)

Mission (Misiones)
├── MissionID (PK)
├── Title
├── Description
└── Difficulty (Easy, Medium, Hard)

Inventory (Inventario - Many-to-Many)
├── CharacterID (PK, FK → Character)
├── ItemID (PK, FK → Item)
└── Quantity

CharacterMission (Asignación de misiones - Many-to-Many)
├── CharacterID (PK, FK → Character)
├── MissionID (PK, FK → Mission)
├── Status (Incomplete, In Progress, Complete)
├── StartDate
└── CompletionDate

Transaction (Transacciones entre personajes)
├── TransactionID (PK)
├── GiverID (FK → Character)
├── ReceiverID (FK → Character)
├── ItemID (FK → Item)
├── TransactionDate
└── TransactionType (Trade, Purchase, Donation)
```

### Relaciones

- **Player → Character**: 1 a N (Un jugador puede tener múltiples personajes)
- **Character → Inventory → Item**: Many-to-Many (Personajes tienen múltiples items)
- **Character → CharacterMission → Mission**: Many-to-Many (Personajes tienen múltiples misiones)
- **Character → Transaction**: Self-referencing (Personajes intercambian items entre sí)

## 🛠️ Tecnologías

### Backend
- **Flask 3.0** - Framework web
- **SQLAlchemy 2.0** - ORM para base de datos
- **Flask-Marshmallow** - Serialización/Deserialización
- **PyMySQL** - Conector MySQL
- **Flask-Migrate** - Migraciones de base de datos

### Frontend
- **Streamlit 1.29** - Framework para interfaces web
- **Pandas 2.0** - Análisis y manipulación de datos
- **Requests** - Cliente HTTP

### Base de Datos
- **MySQL 8.0** - Sistema de gestión de base de datos relacional

### DevOps
- **Docker** - Contenedorización
- **Docker Compose** - Orquestación de contenedores

## 🚀 Instalación

### Opción 1: Con Docker (Recomendado)

#### Requisitos Previos
- Docker Desktop (Windows/Mac) o Docker Engine (Linux)
- Docker Compose
- Git

#### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/game-database-manager.git
cd game-database-manager

# 2. Navegar a la carpeta de Docker
cd DockerFiles

# 3. Crear archivo de variables de entorno (opcional)
cp .env.example .env
# Editar .env si deseas cambiar puertos o credenciales

# 4. Levantar todos los servicios
docker-compose up -d --build

# 5. Verificar que los contenedores están corriendo
docker-compose ps

# Deberías ver:
# - gamedb_mysql
# - gamedb_api
# - gamedb_frontend
```

**¡Listo!** Accede a http://localhost:8501

#### Comandos Útiles

```bash
# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f api

# Reiniciar servicios
docker-compose restart

# Detener servicios
docker-compose down

# Detener y eliminar datos (reset completo)
docker-compose down -v

# Reconstruir un servicio específico
docker-compose up -d --build api
```

### Opción 2: Instalación Local

#### Requisitos Previos
- Python 3.11+
- MySQL 8.0+
- pip

#### Backend (API Flask)

```bash
# 1. Crear entorno virtual
python -m venv .venv

# 2. Activar entorno virtual
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar base de datos
# Editar API/app/config.py con tus credenciales MySQL

# 5. Ejecutar API
cd API
python run.py
```

#### Frontend (Streamlit)

```bash
# En otra terminal

# 1. Activar entorno virtual
source .venv/bin/activate  # o .venv\Scripts\activate en Windows

# 2. Instalar dependencias del frontend
cd frontend
pip install -r requirements.txt

# 3. Ejecutar Streamlit
streamlit run main.py
```

#### Base de Datos

```bash
# 1. Crear la base de datos
mysql -u root -p < BaseCodeSQL/script_project.sql

# 2. Cargar datos de prueba (opcional)
mysql -u root -p GAME_DATABASE < BaseCodeSQL/Test_data.sql
```

## 📖 Uso

### Flujo de Trabajo Básico

1. **Acceder a la aplicación**: http://localhost:8501

2. **Crear un Jugador**
   - Ir a "Players" en el menú lateral
   - Click en "➕ Crear Jugador"
   - Llenar el formulario
   - Guardar

3. **Crear un Personaje**
   - Ir a "Characters"
   - Seleccionar el jugador creado
   - Asignar nombre y atributos
   - Crear

4. **Agregar Items**
   - Ir a "Items"
   - Crear diferentes tipos de items
   - Variar tipos y rarezas

5. **Asignar Items al Inventario**
   - Ir a "Inventory"
   - Seleccionar personaje e item
   - Definir cantidad

6. **Crear y Asignar Misiones**
   - Crear misiones en "Missions"
   - Asignar a personajes en "Character Missions"
   - Actualizar estados

7. **Registrar Transacciones**
   - Ir a "Transactions"
   - Seleccionar donador y receptor
   - Elegir item y tipo de transacción

8. **Ver Reportes**
   - Ir a "Reports"
   - Seleccionar tipo de reporte
   - Analizar datos con JOINs

## 🔌 Endpoints API

### Base URL
```
http://localhost:5000
```

### Players

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/players/` | Obtener todos los jugadores |
| GET | `/players/<id>` | Obtener jugador por ID |
| POST | `/players/` | Crear nuevo jugador |
| PUT | `/players/<id>` | Actualizar jugador |
| DELETE | `/players/<id>` | Eliminar jugador |

### Characters

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/characters/` | Obtener todos los personajes |
| GET | `/characters/<id>` | Obtener personaje por ID |
| POST | `/characters/` | Crear nuevo personaje |
| PUT | `/characters/<id>` | Actualizar personaje |
| DELETE | `/characters/<id>` | Eliminar personaje |

### Items

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/items/` | Obtener todos los items |
| GET | `/items/<id>` | Obtener item por ID |
| POST | `/items/` | Crear nuevo item |
| PUT | `/items/<id>` | Actualizar item |
| DELETE | `/items/<id>` | Eliminar item |

### Missions

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/missions/` | Obtener todas las misiones |
| GET | `/missions/<id>` | Obtener misión por ID |
| POST | `/missions/` | Crear nueva misión |
| PUT | `/missions/<id>` | Actualizar misión |
| DELETE | `/missions/<id>` | Eliminar misión |

### Inventory

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/inventory/` | Obtener todo el inventario |
| GET | `/inventory/<char_id>/<item_id>` | Obtener inventario específico |
| POST | `/inventory/` | Crear entrada de inventario |
| PUT | `/inventory/<char_id>/<item_id>` | Actualizar inventario |
| DELETE | `/inventory/<char_id>/<item_id>` | Eliminar del inventario |

### Character Missions

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/char_missions/` | Obtener todas las asignaciones |
| GET | `/char_missions/<char_id>/<mission_id>` | Obtener asignación específica |
| POST | `/char_missions/` | Crear asignación |
| PUT | `/char_missions/<char_id>/<mission_id>` | Actualizar asignación |
| DELETE | `/char_missions/<char_id>/<mission_id>` | Eliminar asignación |

### Transactions

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/transactions/` | Obtener todas las transacciones |
| GET | `/transactions/<id>` | Obtener transacción por ID |
| POST | `/transactions/` | Crear transacción |
| PUT | `/transactions/<id>` | Actualizar transacción |
| DELETE | `/transactions/<id>` | Eliminar transacción |

### Reports (JOINs)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/reports/` | Lista de reportes disponibles |
| GET | `/reports/characters-with-players` | JOIN Character + Player |
| GET | `/reports/inventory-details` | JOIN Inventory + Character + Item + Player |
| GET | `/reports/missions-progress` | JOIN CharacterMission + Character + Mission + Player |
| GET | `/reports/transactions-details` | JOIN Transaction + Characters + Item |
| GET | `/reports/player-statistics` | Estadísticas agregadas (GROUP BY) |
| GET | `/reports/character-profile/<id>` | Perfil completo de personaje |
| GET | `/reports/items-distribution` | Distribución de items (GROUP BY) |

### Ejemplo de Petición

```bash
# Crear un jugador
curl -X POST http://localhost:5000/players/ \
  -H "Content-Type: application/json" \
  -d '{
    "UserName": "alice",
    "Email": "alice@example.com",
    "RegistrationDate": "2025-01-15"
  }'

# Obtener todos los personajes
curl http://localhost:5000/characters/

# Obtener reporte de inventario detallado
curl http://localhost:5000/reports/inventory-details
```

## 📊 Reportes

### 1. Personajes con Jugadores
**JOIN**: `Character ⟕ Player`

Muestra todos los personajes con información de sus jugadores propietarios.

```sql
SELECT 
    c.CharacterID, c.Name AS CharacterName, c.Level, c.Experience,
    p.PlayerID, p.UserName, p.Email
FROM Character c
INNER JOIN Player p ON c.PlayerID = p.PlayerID
```

### 2. Inventario Detallado
**JOIN**: `Inventory ⟕ Character ⟕ Item ⟕ Player`

Vista completa del inventario con nombres de personajes, jugadores e items.

```sql
SELECT 
    i.CharacterID, c.Name AS CharacterName, p.UserName,
    it.ItemID, it.Name AS ItemName, it.Type, it.Rarity, i.Quantity
FROM Inventory i
INNER JOIN Character c ON i.CharacterID = c.CharacterID
INNER JOIN Player p ON c.PlayerID = p.PlayerID
INNER JOIN Item it ON i.ItemID = it.ItemID
```

### 3. Progreso de Misiones
**JOIN**: `CharacterMission ⟕ Character ⟕ Mission ⟕ Player`

Estado actual de todas las misiones asignadas a personajes.

```sql
SELECT 
    cm.CharacterID, c.Name AS CharacterName, p.UserName,
    cm.MissionID, m.Title, m.Difficulty, cm.Status,
    cm.StartDate, cm.CompletionDate
FROM CharacterMission cm
INNER JOIN Character c ON cm.CharacterID = c.CharacterID
INNER JOIN Player p ON c.PlayerID = p.PlayerID
INNER JOIN Mission m ON cm.MissionID = m.MissionID
```

### 4. Transacciones Detalladas
**SELF JOIN**: `Transaction ⟕ Character (Giver) ⟕ Character (Receiver) ⟕ Item`

Historial completo de intercambios entre personajes con nombres legibles.

```sql
SELECT 
    t.TransactionID, 
    cg.Name AS GiverName, 
    cr.Name AS ReceiverName,
    i.Name AS ItemName, i.Type, i.Rarity,
    t.TransactionDate, t.TransactionType
FROM Transaction t
INNER JOIN Character cg ON t.GiverID = cg.CharacterID
INNER JOIN Character cr ON t.ReceiverID = cr.CharacterID
INNER JOIN Item i ON t.ItemID = i.ItemID
```

### 5. Estadísticas por Jugador
**GROUP BY con Agregaciones**

Métricas agregadas de cada jugador (COUNT, SUM, AVG, MAX).

```sql
SELECT 
    p.PlayerID, p.UserName, p.Email,
    COUNT(c.CharacterID) AS TotalCharacters,
    COALESCE(SUM(c.Level), 0) AS TotalLevels,
    COALESCE(AVG(c.Level), 0) AS AverageLevel,
    COALESCE(MAX(c.Level), 0) AS MaxLevel
FROM Player p
LEFT JOIN Character c ON p.PlayerID = c.PlayerID
GROUP BY p.PlayerID, p.UserName, p.Email
```

### 6. Perfil Completo de Personaje
**Múltiples JOINs Relacionados**

Vista 360° de un personaje específico: info básica, inventario, misiones y transacciones.

### 7. Distribución de Items
**GROUP BY por Tipo y Rareza**

Análisis de cuántos items existen y quién los tiene.

```sql
SELECT 
    i.ItemID, i.Name AS ItemName, i.Type, i.Rarity,
    COUNT(inv.CharacterID) AS TotalOwners,
    COALESCE(SUM(inv.Quantity), 0) AS TotalQuantity
FROM Item i
LEFT JOIN Inventory inv ON i.ItemID = inv.ItemID
GROUP BY i.ItemID, i.Name, i.Type, i.Rarity
```

## 📁 Estructura del Proyecto

```
game-database-manager/
│
├── API/                          # Backend Flask
│   ├── app/
│   │   ├── __init__.py          # Factory de la aplicación
│   │   ├── config.py            # Configuración (DB, etc.)
│   │   └── extensions.py        # SQLAlchemy, Marshmallow
│   │
│   ├── models/                   # Modelos de base de datos
│   │   ├── __init__.py
│   │   ├── player.py
│   │   ├── character.py
│   │   ├── item.py
│   │   ├── mission.py
│   │   ├── inventory.py
│   │   ├── char_mission.py
│   │   └── transaction.py
│   │
│   ├── schemas/                  # Schemas de Marshmallow
│   │   ├── __init__.py
│   │   ├── player_schema.py
│   │   ├── character_schema.py
│   │   ├── item_schema.py
│   │   ├── mission_schema.py
│   │   ├── inventory_schema.py
│   │   ├── char_mission_schema.py
│   │   └── transaction_schema.py
│   │
│   ├── routes/                   # Blueprints (endpoints)
│   │   ├── __init__.py
│   │   ├── player_routes.py
│   │   ├── character_routes.py
│   │   ├── item_routes.py
│   │   ├── mission_routes.py
│   │   ├── inventory_routes.py
│   │   ├── char_mission_routes.py
│   │   ├── transaction_routes.py
│   │   └── reports_routes.py     # ⭐ Reportes con JOINs
│   │
│   ├── services/                 # Lógica de negocio
│   │   ├── player_services.py
│   │   ├── character_services.py
│   │   ├── item_services.py
│   │   ├── mission_services.py
│   │   ├── inventory_services.py
│   │   ├── char_mission_services.py
│   │   ├── transaction_services.py
│   │   └── reports_services.py   # ⭐ Lógica de reportes
│   │
│   └── run.py                    # Punto de entrada de la API
│
├── frontend/                     # Frontend Streamlit
│   ├── components/
│   │   ├── __init__.py
│   │   └── api_client.py        # Cliente HTTP para la API
│   │
│   ├── pages/                    # Páginas de la interfaz
│   │   ├── 1_Players.py
│   │   ├── 2_Character.py
│   │   ├── 3_Item.py
│   │   ├── 4_Transaction.py
│   │   ├── 5_Inventory.py
│   │   ├── 6_Mission.py
│   │   ├── 7_CharacterMission.py
│   │   └── 8_Reports.py         # ⭐ Página de reportes
│   │
│   ├── main.py                   # Página principal
│   └── requirements.txt
│
├── BaseCodeSQL/                  # Scripts de base de datos
│   ├── script_project.sql       # Schema de la DB
│   └── Test_data.sql            # Datos de prueba
│
├── DockerFiles/                  # Configuración Docker
│   ├── docker-compose.yml       # Orquestación de servicios
│   ├── Dockerfile.api           # Imagen de Flask
│   ├── Dockerfile.frontend      # Imagen de Streamlit
│   ├── .env.example             # Template de variables
│   └── README_DOCKER.md
│
├── requirements.txt              # Dependencias del backend
├── .gitignore
└── README.md                     # Este archivo
```
