from extension import db

class Doctor(db.Model):
    __tablename__ = "Doctor"

    EmployeeID = db.Column(db.Integer, db.ForeignKey("Employee.EmployeeID"), primary_key=True)
    SpecialtyID = db.Column(db.Integer, db.ForeignKey("Specialties.SpecialtyID"))
    
    # الحقول الجديدة التي أضفناها لقاعدة البيانات
    Bio = db.Column(db.Text, nullable=True)
    ExperienceYears = db.Column(db.Integer, nullable=True)
    Rating = db.Column(db.Numeric(precision=2, scale=1), nullable=True)
    ProfileImage = db.Column(db.LargeBinary, nullable=True)