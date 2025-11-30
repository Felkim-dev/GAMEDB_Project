import os

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://gameuser:gamepassword@localhost:8080/GAME_DATABASE"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
