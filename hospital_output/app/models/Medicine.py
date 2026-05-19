class Medicine(db.Model):
    __tablename__ = "Medicine"

    MedicineID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Description = db.Column(db.Text)