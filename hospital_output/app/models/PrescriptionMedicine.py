
class PrescriptionMedicine(db.Model):
    __tablename__ = "PrescriptionMedicine"

    PrescriptionID = db.Column(db.Integer, db.ForeignKey("Prescription.PrescriptionID"), primary_key=True)
    MedicineID = db.Column(db.Integer, db.ForeignKey("Medicine.MedicineID"), primary_key=True)
    Dosage = db.Column(db.String(100))
    Duration = db.Column(db.String(100))
