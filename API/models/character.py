from ..app.extensions import db

class Character(db.Model):
    # TODO: definir la clase
    __tablename__="Character_1"
    character_id=db.Column(db.Integer, primary_key=True)
    #agregar backref a player.py
    player_id=db.Column(db.Integer, db.ForeignKey("Player.player_id"))
    character_name=db.Column(db.String(50), nullable=False)
    character_level=db.Column(db.Integer, nullable=False)
    character_experience=db.Column(db.Integer, nullable=False)

    #metodo para instanciar un objeto de tipo Character
    def __init__(self,player_id,character_name,character_level,character_experience):
        self.player_id=player_id
        self.character_name=character_name
        self.character_level=character_level
        self.character_experience=character_experience
    #TODO: definir el def create en la carpeta services para estructura mas limpia