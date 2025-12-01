import os

class Config:
    # Usar variable de entorno si está disponible, sino usar valor por defecto
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://gameuser:gamepassword@localhost:8080/GAME_DATABASE",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
