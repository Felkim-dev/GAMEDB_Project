from app.extensions import db

class Mission(db.Model):
    # TODO: definir la clase
    __tablename__="Mission"
    MissionID=db.Column(db.Integer, primary_key=True)
    Title=db.Column(db.String(100), nullable=False)
    Description=db.Column(db.String(1000), nullable=False)
    Difficulty=db.Column(db.Enum('Easy', 'Medium', 'Hard'), nullable=False)

    #Relaciones
    characters_link = db.relationship("CharacterMission", back_populates="mission")
    
    #metodo para instanciar un objeto de tipo Character
    def __init__(self,Title,Description,Difficulty):
        self.Title=Title 
        self.Description=Description
        self.Difficulty=Difficulty

