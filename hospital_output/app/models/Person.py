class Person(db.Model):
    __tablename__ = "Person"

    PersonID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(100))
    LastName = db.Column(db.String(100))
    Gender = db.Column(db.String(10))
    Email = db.Column(db.String(150))
    Phone = db.Column(db.String(20))
    Address = db.Column(db.String(200))