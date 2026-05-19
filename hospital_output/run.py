# from flask import Flask, Response, redirect, render_template, request, url_for, session
# from app.models.Department import Department
# from extension import db
# from app.models.Users import Users
# from config import Config
# from app.models.Speciality import Specialties
# from sqlalchemy import text
# from werkzeug.security import check_password_hash, generate_password_hash


# app = Flask(__name__)
# app.config.from_object(Config)

# app.secret_key = "mysecretkey123"   # ✅ أضف هذا السطر
# db.init_app(app)

# # ==========================
# # Sign UP Page
# # ==========================
# # @app.route("/signup", methods=["GET","POST"])
# # def signup():

# #     if request.method == "POST":

# #         first = request.form["first_name"]
# #         last = request.form["last_name"]
# #         gender = request.form["gender"]
# #         email = request.form["email"]
# #         phone = request.form["phone"]
# #         address = request.form["address"]
# #         dob = request.form["dob"]
# #         blood = request.form["blood_type"]
# #         password = request.form["password"]
# #         confirm = request.form["confirm_password"]

# #         if password != confirm:
# #             return "Passwords do not match"

# #         # 🔐 تشفير الباسورد
# #         hashed_password = generate_password_hash(password)

# #         # ❗ تحقق هل الإيميل موجود
# #         check_user = db.session.execute(
# #             text("SELECT UserID FROM Users WHERE Email=:email"),
# #             {"email": email}
# #         ).fetchone()

# #         if check_user:
# #             return "Email already exists"

# #         # 1️⃣ Person
# #         result = db.session.execute(text("""
# #         INSERT INTO Person (FirstName, LastName, Gender, Email, Phone, Address)
# #         OUTPUT INSERTED.PersonID
# #         VALUES (:first, :last, :gender, :email, :phone, :address)
# #         """), {
# #             "first": first,
# #             "last": last,
# #             "gender": gender,
# #             "email": email,
# #             "phone": phone,
# #             "address": address
# #         })

# #         person_id = result.fetchone()[0]

# #         # 2️⃣ Patient
# #         db.session.execute(text("""
# #         INSERT INTO Patient (PersonID, DateOfBirth, BloodType)
# #         VALUES (:pid, :dob, :blood)
# #         """), {
# #             "pid": person_id,
# #             "dob": dob,
# #             "blood": blood
# #         })

# #         # 3️⃣ Users
# #         db.session.execute(text("""
# #         INSERT INTO Users (PersonID, Email, PasswordHash, Role, IsActive)
# #         VALUES (:pid, :email, :password, 'Patient', 1)
# #         """), {
# #             "pid": person_id,
# #             "email": email,
# #             "password": hashed_password
# #         })

# #         db.session.commit()

# #         return redirect(url_for("login"))

# #     return render_template("signup.html")

# @app.route("/signup", methods=["GET","POST"])
# def signup():

#     if request.method == "POST":

#         first = request.form["first_name"]
#         last = request.form["last_name"]
#         gender = request.form["gender"]
#         email = request.form["email"]
#         phone = request.form["phone"]
#         address = request.form["address"]
#         dob = request.form["dob"]
#         blood = request.form["blood_type"]
#         password = request.form["password"]
#         confirm = request.form["confirm_password"]

#         if password != confirm:
#             return "Passwords do not match"

#         # ❗ تحقق هل الإيميل موجود
#         check_user = db.session.execute(
#             text("SELECT UserID FROM Users WHERE Email=:email"),
#             {"email": email}
#         ).fetchone()

#         if check_user:
#             return "Email already exists"

#         # 1️⃣ Person
#         result = db.session.execute(text("""
#         INSERT INTO Person (FirstName, LastName, Gender, Email, Phone, Address)
#         OUTPUT INSERTED.PersonID
#         VALUES (:first, :last, :gender, :email, :phone, :address)
#         """), {
#             "first": first,
#             "last": last,
#             "gender": gender,
#             "email": email,
#             "phone": phone,
#             "address": address
#         })

#         person_id = result.fetchone()[0]

#         # 2️⃣ Patient
#         db.session.execute(text("""
#         INSERT INTO Patient (PersonID, DateOfBirth, BloodType)
#         VALUES (:pid, :dob, :blood)
#         """), {
#             "pid": person_id,
#             "dob": dob,
#             "blood": blood
#         })

#         # 3️⃣ Users (بدون hash)
#         db.session.execute(text("""
#         INSERT INTO Users (PersonID, Email, PasswordHash, Role, IsActive)
#         VALUES (:pid, :email, :password, 'Patient', 1)
#         """), {
#             "pid": person_id,
#             "email": email,
#             "password": password   # ✅ بدون تشفير
#         })

#         db.session.commit()

#         return redirect(url_for("login"))

#     return render_template("signup.html")
# #without hash
# # ==========================
# # Login Page
# # ==========================
# # @app.route("/login", methods=["GET", "POST"])
# # def login():

# #     error = None  

# #     if request.method == "POST":

# #         email = request.form.get("email")
# #         password = request.form.get("password")

# #         user = Users.query.filter_by(Email=email).first()

# #         if not user:
# #             error = "User does not exist"

# #         elif user.PasswordHash != password:
# #             error = "Wrong password"

# #         else:
# #             return redirect(url_for("home_page"))

# #     return render_template("login.html", error=error) 
# #login with hash
# @app.route("/login", methods=["GET", "POST"])
# def login():

#     error = None  

#     if request.method == "POST":

#         email = request.form.get("email")
#         password = request.form.get("password")

#         user = Users.query.filter_by(Email=email).first()

#         if not user:
#             error = "User does not exist"

#         elif user.PasswordHash != password:
#             error = "Wrong password"

#         else:
#             session["user_id"] = user.UserID
#             session["role"] = user.Role

#             return redirect(url_for("home_page"))

#     return render_template("login.html", error=error)

# # ==========================
# # Logout
# # ==========================
# @app.route("/logout")
# def logout():
#     session.clear()
#     return redirect(url_for("login"))


# # ==========================
# # Home
# # ==========================
# @app.route("/")
# def home():
    
   
#         return redirect((url_for("login")))
   
# @app.route("/home")
# def home_page():
   
#     return render_template("index.html")   

# # ==========================login
# # Specialties
# # ==========================
# @app.route("/specialties")
# def specialties():
   
#     specialties = Specialties.query.all()
#     return render_template("specialties.html", specialties=specialties)


# # ==========================
# # باقي الصفحات (بدون تغيير)
# # ==========================

# @app.route("/about")
# def about_page():
    
#     return render_template("about.html")


# @app.route("/departments")
# def departments_page():
   
#     return render_template("specialties.html")


# @app.route("/doctor_image/<int:id>")
# def doctor_image(id):
#     doctor = db.session.execute(
#         text("SELECT ProfileImage FROM Doctor WHERE EmployeeID=:id"),
#         {"id": id}
#     ).fetchone()
#     return Response(doctor.ProfileImage, mimetype="image/jpeg")


# @app.route("/doctors")
# def doctors_page():
#     if "user_id" not in session:
#         return redirect(url_for("login"))

#     specialty = request.args.get("specialty")

#     if specialty:
#         doctors = db.session.execute(text("""
#         SELECT d.EmployeeID, p.FirstName, p.LastName, p.Gender,
#                s.Name AS Specialty, d.Bio, d.ExperienceYears,
#                d.ProfileImage, d.Rating
#         FROM Doctor d
#         JOIN Employee e ON d.EmployeeID = e.EmployeeID
#         JOIN Person p ON e.PersonID = p.PersonID
#         JOIN Specialties s ON d.SpecialtyID = s.SpecialtyID
#         WHERE s.Name = :specialty
#         """), {"specialty": specialty}).fetchall()
#     else:
#         doctors = db.session.execute(text("""
#         SELECT d.EmployeeID, p.FirstName, p.LastName, p.Gender,
#                s.Name AS Specialty, d.Bio, d.ExperienceYears,
#                d.ProfileImage, d.Rating
#         FROM Doctor d
#         JOIN Employee e ON d.EmployeeID = e.EmployeeID
#         JOIN Person p ON e.PersonID = p.PersonID
#         JOIN Specialties s ON d.SpecialtyID = s.SpecialtyID
#         """)).fetchall()

#     return render_template("doctors.html", doctors=doctors)


# @app.route("/book_appointment", methods=["POST"])
# def book_appointment():
#     if "user_id" not in session:
#         return redirect(url_for("login"))

#     name = request.form["full_name"]
#     email = request.form["email"]
#     reason = request.form["reason"]
#     date = request.form["date"]
#     time = request.form["time"]

#     db.session.execute(text("""
#     INSERT INTO Appointment
#     (DoctorID, PatientName, PatientEmail, VisitReason, AppointmentDate, AppointmentTime)
#     VALUES (1, :name, :email, :reason, :date, :time)
#     """), {
#         "name": name,
#         "email": email,
#         "reason": reason,
#         "date": date,
#         "time": time
#     })

#     db.session.commit()
#     return redirect(url_for("doctors_page"))


# @app.route("/patient")
# def patient_page():
#     if "user_id" not in session:
#         return redirect(url_for("login"))
#     return render_template("patient.html")


# @app.route("/appointment")
# def appointment_page():
#     if "user_id" not in session:
#         return redirect(url_for("login"))
#     return render_template("patient.html")


# @app.route("/contact")
# def contact_page():
#     if "user_id" not in session:
#         return redirect(url_for("login"))
#     return render_template("contact.html")


# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask
from config import Config
from extension import db

from app.routes.auth_routes import auth_bp
from app.routes.doctor_routes import doctor_bp
from app.routes.patient_routes import patient_bp
from app.routes.specialty_routes import specialty_bp
from app.routes.appointment_routes import appointment_bp
from app.routes.main_routes import main_bp   

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.secret_key = "mysecretkey123"

    db.init_app(app)

    # ==========================
    # Register Blueprints
    # ==========================
    app.register_blueprint(auth_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(specialty_bp)
    app.register_blueprint(appointment_bp)
    app.register_blueprint(main_bp)   

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

#make a list of appoinment 