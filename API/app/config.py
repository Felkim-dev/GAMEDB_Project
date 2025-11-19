import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:steve@localhost:3307/GAME_DATABASE'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
