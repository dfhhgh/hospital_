class MedicineStock(db.Model):
    __tablename__ = "MedicineStock"

    MedicineID = db.Column(db.Integer, db.ForeignKey("Medicine.MedicineID"), primary_key=True)
    Quantity = db.Column(db.Integer)
    Price = db.Column(db.Float)
    ExpireDate = db.Column(db.Date)