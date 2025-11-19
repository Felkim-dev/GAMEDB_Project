from app.extensions import db

class Player(db.Model):
    __tablename__ = "Player"
    player_id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(50), nullable=False)
    email=db.Column(db.String(50), nullable=False)
    registration_date=db.Column(db.Date, nullable=False)

    def __init__(self,username,email,registration_date):
        self.username=username
        self.email=email
        self.registration_date=registration_date
    
    #TODO: definir el def create en la carpeta services para estructura mas limpia
