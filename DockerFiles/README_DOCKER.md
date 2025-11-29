# Docker Setup para GAME_DATABASE

## Requisitos Previos

- Docker instalado
- Docker Compose instalado

## Configuración Rápida

### 1. Navegar a la carpeta DockerFiles

```bash
cd DockerFiles
```

### 2. Construir y levantar el contenedor

```bash
docker-compose up -d
```

### 3. Verificar que está corriendo

```bash
docker ps
```

### 4. Conectar a la base de datos

**Desde tu máquina (host):**

```bash
mysql -h 127.0.0.1 -P 8080 -u gameuser -p
# Password: gamepassword
```

**Desde Python (Flask API):**

```python
SQLALCHEMY_DATABASE_URI = 'mysql://gameuser:gamepassword@localhost:8080/GAME_DATABASE'
```

**Desde MySQL Workbench:**

- Host: `127.0.0.1` o `localhost`
- Port: `8080`
- User: `gameuser`
- Password: `gamepassword`
- Database: `GAME_DATABASE`

## Comandos Útiles

### Ver logs del contenedor

```bash
docker-compose logs -f mysql
```

### Detener el contenedor

```bash
docker-compose down
```

### Detener y eliminar datos (reiniciar desde cero)

```bash
docker-compose down -v
```

### Acceder al contenedor

```bash
docker exec -it gamedb_mysql bash
```

### Ejecutar comandos SQL directamente

```bash
docker exec -it gamedb_mysql mysql -u root -prootpassword GAME_DATABASE
```

### Backup de la base de datos

```bash
docker exec gamedb_mysql mysqldump -u root -prootpassword GAME_DATABASE > backup.sql
```

### Restaurar desde backup

```bash
docker exec -i gamedb_mysql mysql -u root -prootpassword GAME_DATABASE < backup.sql
```

## Estructura de Archivos

```
GAMEDB_Project/
├── DockerFiles/
│   ├── Dockerfile              # Configuración de la imagen MySQL
│   ├── docker-compose.yml      # Orquestación del contenedor
│   ├── .env.example           # Variables de entorno (copia a .env)
│   └── README_DOCKER.md       # Esta guía
└── BaseCodeSQL/
    └── script_project.sql     # Se ejecuta automáticamente al crear el contenedor
```

## Configuración de Seguridad

⚠️ **IMPORTANTE:** Las contraseñas en los archivos son solo para desarrollo.

Para producción:

1. Copia `.env.example` a `.env`
2. Cambia las contraseñas
3. Agrega `.env` al `.gitignore`

## Solución de Problemas

### Puerto 8080 ya en uso

Edita `docker-compose.yml` y cambia:

```yaml
ports:
  - "8080:3306" # Cambia 8080 por otro puerto disponible
```

### El script SQL no se ejecuta

```bash
docker-compose down -v
docker-compose up -d
```

### Ver errores de MySQL

```bash
docker-compose logs mysql
```
