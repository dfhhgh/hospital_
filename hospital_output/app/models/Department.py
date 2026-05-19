from extension import db
class Department(db.Model):
    __tablename__ = "Department"

    DepartmentID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Location = db.Column(db.String(100))
    def __repr__(self):
        return f"<Department {self.Name}>"

    # ------------------------
    # GET ALL
    # ------------------------
    @staticmethod
    def get_all():
        return Department.query.all()