class MedicalRecord(db.Model):
    __tablename__ = "MedicalRecord"

    RecordID = db.Column(db.Integer, primary_key=True)
    PatientID = db.Column(db.Integer, db.ForeignKey("Patient.PersonID"))
    DoctorID = db.Column(db.Integer, db.ForeignKey("Doctor.EmployeeID"))
    VisitDate = db.Column(db.DateTime)
    Notes = db.Column(db.Text)