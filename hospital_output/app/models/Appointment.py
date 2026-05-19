class Appointment(db.Model):
    __tablename__ = "Appointment"

    AppointmentID = db.Column(db.Integer, primary_key=True)
    PatientID = db.Column(db.Integer, db.ForeignKey("Patient.PersonID"))
    DoctorID = db.Column(db.Integer, db.ForeignKey("Doctor.EmployeeID"))
    AppointmentDate = db.Column(db.DateTime)
    StatusID = db.Column(db.Integer, db.ForeignKey("AppointmentStatus.StatusID"))
    Notes = db.Column(db.Text)