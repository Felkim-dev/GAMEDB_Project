from app.extensions import db

class Character(db.Model):
    # TODO: definir la clase
    __tablename__="Character_1"
    CharacterID=db.Column(db.Integer, primary_key=True)
    PlayerID=db.Column(db.Integer, db.ForeignKey("Player.PlayerID"))
    Name=db.Column(db.String(50), nullable=False)
    Level=db.Column(db.Integer, nullable=False)
    Experience=db.Column(db.Integer, nullable=False)

    #metodo para instanciar un objeto de tipo Character
    def __init__(self,PlayerID,Name,Level,Experience):
        self.PlayerID=PlayerID
        self.Name=Name
        self.Level=Level
        self.Experience=Experience
    #TODO: definir el def create en la carpeta services para estructura mas limpia