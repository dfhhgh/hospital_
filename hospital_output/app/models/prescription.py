class Prescription(db.Model):
    __tablename__ = "Prescription"

    PrescriptionID = db.Column(db.Integer, primary_key=True)
    AppointmentID = db.Column(db.Integer, db.ForeignKey("Appointment.AppointmentID"))
    DoctorID = db.Column(db.Integer, db.ForeignKey("Doctor.EmployeeID"))
    PatientID = db.Column(db.Integer, db.ForeignKey("Patient.PersonID"))
    DateIssued = db.Column(db.DateTime)
