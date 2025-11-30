from app.extensions import db

class Player(db.Model):
    __tablename__ = "Player"
    PlayerID=db.Column(db.Integer, primary_key=True)
    UserName=db.Column(db.String(50), nullable=False)
    Email=db.Column(db.String(50), nullable=False)
    RegistrationDate=db.Column(db.Date, nullable=False)
    #backreference a Character, prueba
    characters=db.relationship('Character',back_populates='player',passive_deletes=True)

    def __init__(self,UserName,Email,RegistrationDate):
        self.UserName=UserName
        self.Email=Email
        self.RegistrationDate=RegistrationDate
    
    #TODO: definir el def create en la carpeta services para estructura mas limpia
