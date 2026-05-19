
class Employee(db.Model):
    __tablename__ = "Employee"

    EmployeeID = db.Column(db.Integer, primary_key=True)
    PersonID = db.Column(db.Integer, db.ForeignKey("Person.PersonID"))
    DepartmentID = db.Column(db.Integer, db.ForeignKey("Department.DepartmentID"))
    HireDate = db.Column(db.Date)
    Salary = db.Column(db.Float)
    JobTitle = db.Column(db.String(100))