import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:steve@127.0.0.1:3307/GAME_DATABASE'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
