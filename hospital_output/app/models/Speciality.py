from extension import db


class Specialties(db.Model):
    __tablename__ = "Specialties"

    SpecialtyID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))