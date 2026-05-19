class Admission(db.Model):
    __tablename__ = "Admission"

    AdmissionID = db.Column(db.Integer, primary_key=True)
    PatientID = db.Column(db.Integer, db.ForeignKey("Patient.PersonID"))
    RoomID = db.Column(db.Integer, db.ForeignKey("Room.RoomID"))
    DoctorID = db.Column(db.Integer, db.ForeignKey("Doctor.EmployeeID"))
    AdmissionDate = db.Column(db.DateTime)
    DischargeDate = db.Column(db.DateTime)
    Status = db.Column(db.String(50))