class Patient(db.Model):
    __tablename__ = "Patient"

    PersonID = db.Column(db.Integer, db.ForeignKey("Person.PersonID"), primary_key=True)
    DateOfBirth = db.Column(db.Date)
    BloodType = db.Column(db.String(5))