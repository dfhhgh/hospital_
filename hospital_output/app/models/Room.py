class Room(db.Model):
    __tablename__ = "Room"

    RoomID = db.Column(db.Integer, primary_key=True)
    RoomNumber = db.Column(db.String(50))
    Type = db.Column(db.String(50))
    Status = db.Column(db.String(50))
    DepartmentID = db.Column(db.Integer, db.ForeignKey("Department.DepartmentID"))