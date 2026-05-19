from extension import db
from werkzeug.security import check_password_hash

class Users(db.Model):
    __tablename__ = "Users"

    UserID = db.Column(db.Integer, primary_key=True)
    PersonID = db.Column(db.Integer, db.ForeignKey("Person.PersonID"))
    Email = db.Column(db.String(150))
    PasswordHash = db.Column(db.String(255))
    Role = db.Column(db.String(50))
    IsActive = db.Column(db.Boolean)
    CreatedAt = db.Column(db.DateTime)
    
    @staticmethod
    def is_user_exist(email):
     return Users.query.filter_by(Email=email).first() is not None
    
    @staticmethod
    def is_password_correct(email, password):
     user = Users.query.filter_by(Email=email).first()

     if not user:
         return False

     return user.PasswordHash == password