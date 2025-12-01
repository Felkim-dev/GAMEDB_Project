from app.extensions import db


class CharacterMission(db.Model):
    __tablename__ = "CharacterMission"
    CharacterID = db.Column(
        db.Integer,
        db.ForeignKey("Character.CharacterID", ondelete="CASCADE"),
        primary_key=True,
    )
    MissionID = db.Column(
        db.Integer,
        db.ForeignKey("Mission.MissionID", ondelete="CASCADE"),
        primary_key=True,
    )
    Status = db.Column(db.Enum("Incomplete", "In Progress", "Complete"), nullable=False)
    StartDate = db.Column(db.DateTime, default=db.func.current_timestamp())
    CompletionDate = db.Column(db.DateTime, nullable=True)

    # Relaciones
    char_mission = db.relationship("Character", back_populates="missions_link")
    mission = db.relationship("Mission", back_populates="characters_link")

    # metodo para instanciar un objeto de tipo CharacterMission
    def __init__(
        self, CharacterID, MissionID, Status, StartDate=None, CompletionDate=None
    ):
        self.CharacterID = CharacterID
        self.MissionID = MissionID
        self.Status = Status
        self.StartDate = StartDate
        self.CompletionDate = CompletionDate
