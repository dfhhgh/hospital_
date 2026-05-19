class Bill(db.Model):
    __tablename__ = "Bill"

    BillID = db.Column(db.Integer, primary_key=True)
    PatientID = db.Column(db.Integer, db.ForeignKey("Patient.PersonID"))
    AppointmentID = db.Column(db.Integer, db.ForeignKey("Appointment.AppointmentID"))
    Amount = db.Column(db.Float)
    BillDate = db.Column(db.DateTime)
    Status = db.Column(db.String(50))