from flask import request, redirect, url_for, render_template, session
from extension import db
from sqlalchemy import text
from app.models.Users import Users
from werkzeug.security import generate_password_hash, check_password_hash


class AuthService:

    @staticmethod
    def signup():
        if request.method == "POST":

            first = request.form["first_name"]
            last = request.form["last_name"]
            gender = request.form["gender"]
            email = request.form["email"]
            phone = request.form["phone"]
            address = request.form["address"]
            dob = request.form["dob"]
            blood = request.form["blood_type"]
            password = request.form["password"]
            confirm = request.form["confirm_password"]

            if password != confirm:
                return "Passwords do not match"

            # تحقق من وجود الإيميل
            check_user = db.session.execute(
                text("SELECT UserID FROM Users WHERE Email=:email"),
                {"email": email}
            ).fetchone()

            if check_user:
                return "Email already exists"

            # تشفير الباسورد
            hashed_password = password

            # 1️⃣ Person
            db.session.execute(text("""
            INSERT INTO Person (FirstName, LastName, Gender, Email, Phone, Address)
            VALUES (:first, :last, :gender, :email, :phone, :address)
            """), {
                "first": first,
                "last": last,
                "gender": gender,
                "email": email,
                "phone": phone,
                "address": address
            })

            person_id = db.session.execute(text("SELECT LAST_INSERT_ID()")).scalar()

            # 2️⃣ Patient
            db.session.execute(text("""
            INSERT INTO Patient (PersonID, DateOfBirth, BloodType)
            VALUES (:pid, :dob, :blood)
            """), {
                "pid": person_id,
                "dob": dob,
                "blood": blood
            })

            # 3️⃣ Users
            db.session.execute(text("""
            INSERT INTO Users (PersonID, Email, PasswordHash, Role, IsActive)
            VALUES (:pid, :email, :password, 'Patient', 1)
            """), {
                "pid": person_id,
                "email": email,
                "password": hashed_password
            })

            db.session.commit()

            return redirect(url_for("auth.login"))

        return render_template("signup.html")

    @staticmethod
    def login():
        error = None

        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

            user = Users.query.filter_by(Email=email).first()

            if not user:
                error = "User does not exist"

            elif not user.PasswordHash == password:
                error = "Wrong password"

            else:
                session["user_id"] = user.UserID
                session["role"] = user.Role
                return redirect(url_for("main.home_page"))

        return render_template("login.html", error=error)

    @staticmethod
    def logout():
        session.clear()
        return redirect(url_for("auth.login"))