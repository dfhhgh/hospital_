class LabTest(db.Model):
    __tablename__ = "LabTest"

    TestID = db.Column(db.Integer, primary_key=True)
    PatientID = db.Column(db.Integer, db.ForeignKey("Patient.PersonID"))
    DoctorID = db.Column(db.Integer, db.ForeignKey("Doctor.EmployeeID"))
    TestName = db.Column(db.String(100))
    Result = db.Column(db.Text)
    TestDate = db.Column(db.DateTime)