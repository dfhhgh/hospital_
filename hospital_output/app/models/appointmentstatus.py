class AppointmentStatus(db.Model):
    __tablename__ = "AppointmentStatus"

    StatusID = db.Column(db.Integer, primary_key=True)
    StatusName = db.Column(db.String(100))