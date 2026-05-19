class Diagnosis(db.Model):
    __tablename__ = "Diagnosis"

    DiagnosisID = db.Column(db.Integer, primary_key=True)
    PatientID = db.Column(db.Integer, db.ForeignKey("Patient.PersonID"))
    DoctorID = db.Column(db.Integer, db.ForeignKey("Doctor.EmployeeID"))
    DiagnosisText = db.Column(db.Text)
    DiagnosisDate = db.Column(db.DateTime)