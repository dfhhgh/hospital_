from extension import db
from sqlalchemy import text


class DoctorService:

    @staticmethod
    def get_doctors(specialty=None):

        if specialty:
            doctors = db.session.execute(text("""
            SELECT d.EmployeeID, p.FirstName, p.LastName, p.Gender,
                   s.Name AS Specialty, d.Bio, d.ExperienceYears,
                   d.ProfileImage, d.Rating
            FROM Doctor d
            JOIN Employee e ON d.EmployeeID = e.EmployeeID
            JOIN Person p ON e.PersonID = p.PersonID
            JOIN Specialties s ON d.SpecialtyID = s.SpecialtyID
            WHERE s.Name = :specialty
            """), {"specialty": specialty}).fetchall()

        else:
            doctors = db.session.execute(text("""
            SELECT d.EmployeeID, p.FirstName, p.LastName, p.Gender,
                   s.Name AS Specialty, d.Bio, d.ExperienceYears,
                   d.ProfileImage, d.Rating
            FROM Doctor d
            JOIN Employee e ON d.EmployeeID = e.EmployeeID
            JOIN Person p ON e.PersonID = p.PersonID
            JOIN Specialties s ON d.SpecialtyID = s.SpecialtyID
            """)).fetchall()

        return doctors

    @staticmethod
    def get_doctor(id):
        doctor = db.session.execute(text("""
            SELECT d.EmployeeID, p.FirstName, p.LastName, p.Gender,
                   s.Name AS Specialty, d.Bio, d.ExperienceYears,
                   d.ProfileImage, d.Rating
            FROM Doctor d
            JOIN Employee e ON d.EmployeeID = e.EmployeeID
            JOIN Person p ON e.PersonID = p.PersonID
            JOIN Specialties s ON d.SpecialtyID = s.SpecialtyID
            WHERE d.EmployeeID = :id
            """), {"id": id}).fetchone()
        return doctor

# Get doctor profile image by employee ID (on working on doctor profile page)
    @staticmethod
    def get_doctor_image(id):
        doctor = db.session.execute(
            text("SELECT ProfileImage FROM Doctor WHERE EmployeeID=:id"),
            {"id": id}
        ).fetchone()

        return doctor.ProfileImage if doctor else None