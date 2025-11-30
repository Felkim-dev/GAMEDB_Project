from app.extensions import db

class Character(db.Model):
    # TODO: definir la clase
    __tablename__ = "Character"
    CharacterID=db.Column(db.Integer, primary_key=True)
    PlayerID=db.Column(db.Integer, db.ForeignKey("Player.PlayerID",ondelete="CASCADE"), nullable=False)
    Name=db.Column(db.String(50), nullable=False)
    Level=db.Column(db.Integer, nullable=False)
    Experience=db.Column(db.Integer, nullable=False)

    #Relaciones
    #backref de la clase Giver
    #Giver=db.relationship("Giver",backref="Character")
    player=db.relationship("Player", back_populates="characters")
    missions_link = db.relationship("CharacterMission", back_populates="char_mission",passive_deletes=True)
    inventory_holders = db.relationship("Inventory", back_populates="character",passive_deletes=True)
    given_transactions= db.relationship("Transaction", back_populates="giver", foreign_keys='Transaction.GiverID',passive_deletes=True)
    received_transactions= db.relationship("Transaction", back_populates="receiver", foreign_keys='Transaction.ReceiverID',passive_deletes=True)
    #metodo para instanciar un objeto de tipo Character
    def __init__(self,PlayerID,Name,Level,Experience):
        self.PlayerID=PlayerID
        self.Name=Name
        self.Level=Level
        self.Experience=Experience
    #TODO: definir el def create en la carpeta services para estructura mas limpia