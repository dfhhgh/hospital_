from sqlalchemy import text
from extension import db


class PatientService:

    @staticmethod
    def get_profile_by_user_id(user_id):
        result = db.session.execute(
            text(
                """
                SELECT
                    u.UserID,
                    u.Email AS UserEmail,
                    p.PersonID,
                    p.FirstName,
                    p.LastName,
                    p.Gender,
                    p.Email AS PersonEmail,
                    p.Phone,
                    p.Address,
                    pt.DateOfBirth,
                    pt.BloodType
                FROM Users u
                LEFT JOIN Person p ON p.PersonID = u.PersonID
                LEFT JOIN Patient pt ON pt.PersonID = p.PersonID
                WHERE u.UserID = :user_id
                """
            ),
            {"user_id": user_id},
        ).mappings().fetchone()

        if not result:
            return None

        profile = dict(result)
        profile["Email"] = profile.get("PersonEmail") or profile.get("UserEmail")
        return profile

    @staticmethod
    def get_patient_appointments(user_id):
        profile = PatientService.get_profile_by_user_id(user_id)
        if not profile:
            return []

        person_id = profile.get("PersonID")

        result = db.session.execute(text("""
            SELECT 
                a.AppointmentID,
                a.AppointmentDate,
                a.AppointmentTime,
                a.DoctorID,
                s.StatusName,
                CONCAT(p.FirstName, ' ', p.LastName) AS DoctorName,
                p.Email AS DoctorEmail,
                a.PatientEmail AS AppointmentEmail,
                a.StatusID,
                a.Notes,
                a.VisitReason
            FROM Appointment a
            JOIN Doctor d ON a.DoctorID = d.EmployeeID
            JOIN Employee e ON d.EmployeeID = e.EmployeeID
            JOIN Person p ON e.PersonID = p.PersonID
            JOIN AppointmentStatus s ON a.StatusID = s.StatusID
            WHERE a.PatientID = :patient_id
            ORDER BY a.AppointmentDate DESC
        """), {"patient_id": person_id}).mappings().fetchall()

        return [dict(row) for row in result]

    @staticmethod
    def update_profile(user_id, data):
        profile = PatientService.get_profile_by_user_id(user_id)
        if not profile:
            return False, "Profile not found"

        email = data.get("email", "").strip()
        first_name = data.get("first_name", "").strip()
        last_name = data.get("last_name", "").strip()
        gender = data.get("gender", "").strip() or None
        phone = data.get("phone", "").strip() or None
        address = data.get("address", "").strip() or None
        blood_type = data.get("blood_type", "").strip() or None
        dob = data.get("dob", "").strip() or None

        if not first_name or not last_name or not email:
            return False, "First name, last name, and email are required"

        existing_email = db.session.execute(
            text(
                """
                SELECT UserID
                FROM Users
                WHERE Email = :email AND UserID <> :user_id
                """
            ),
            {"email": email, "user_id": user_id},
        ).fetchone()

        if existing_email:
            return False, "Email is already used by another account"

        person_id = profile["PersonID"]

        try:
            db.session.execute(
                text(
                    """
                    UPDATE Person
                    SET FirstName = :first_name,
                        LastName = :last_name,
                        Gender = :gender,
                        Email = :email,
                        Phone = :phone,
                        Address = :address
                    WHERE PersonID = :person_id
                    """
                ),
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    "gender": gender,
                    "email": email,
                    "phone": phone,
                    "address": address,
                    "person_id": person_id,
                },
            )

            db.session.execute(
                text(
                    """
                    UPDATE Users
                    SET Email = :email
                    WHERE UserID = :user_id
                    """
                ),
                {"email": email, "user_id": user_id},
            )

            db.session.execute(
                text(
                    """
                    UPDATE Patient
                    SET DateOfBirth = :dob,
                        BloodType = :blood_type
                    WHERE PersonID = :person_id
                    """
                ),
                {
                    "dob": dob,
                    "blood_type": blood_type,
                    "person_id": person_id,
                },
            )

            db.session.commit()
        except Exception:
            db.session.rollback()
            return False, "Unable to update profile right now"

        return True, "Profile updated successfully"