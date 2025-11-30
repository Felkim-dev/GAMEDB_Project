FROM mysql:latest

# Variables de entorno para la configuración de MySQL
ENV MYSQL_ROOT_PASSWORD=rootpassword
ENV MYSQL_DATABASE=GAME_DATABASE
ENV MYSQL_USER=gameuser
ENV MYSQL_PASSWORD=gamepassword

# Copiar el script SQL al contenedor
COPY BaseCodeSQL/script_project.sql /docker-entrypoint-initdb.d/

# Exponer el puerto 8080 (mapearemos 3306 de MySQL a 8080)
EXPOSE 3306
