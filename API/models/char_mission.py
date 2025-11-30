from app.extensions import db

class CharacterMission(db.Model):
    __tablename__="CharacterMission"
    CharacterID=db.Column(db.Integer, db.ForeignKey('Character.CharacterID'),primary_key=True)
    MissionID=db.Column(db.Integer, db.ForeignKey('Mission.MissionID'), primary_key=True)
    Status=db.Column(db.Integer, nullable=False)

    #Relaciones
    char_mission = db.relationship("Character", back_populates="missions_link")
    mission   = db.relationship("Mission", back_populates="characters_link")


    #metodo para instanciar un objeto de tipo CharacterMission
    def __init__(self,CharacterID,MissionID,Status):
        self.CharacterID=CharacterID 
        self.MissionID=MissionID
        self.Status=Status
    