class Nurse(db.Model):
    __tablename__ = "Nurse"

    EmployeeID = db.Column(db.Integer, db.ForeignKey("Employee.EmployeeID"), primary_key=True)
    Shift = db.Column(db.String(50))