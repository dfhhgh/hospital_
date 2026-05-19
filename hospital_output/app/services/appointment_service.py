from extension import db
from sqlalchemy import text
from datetime import datetime
from app.services.patient_service import PatientService


class AppointmentService:

    @staticmethod
    def get_booked_slots(doctor_id, date_str):
        query = text("""
            SELECT AppointmentTime
            FROM Appointment
            WHERE DoctorID = :doctor_id
            AND CAST(AppointmentDate AS DATE) = :date
            AND StatusID != 3
        """)

        result = db.session.execute(query, {
            "doctor_id": doctor_id,
            "date": date_str
        }).fetchall()

        booked_times = []

        for row in result:
            time_value = row[0]

            if hasattr(time_value, "strftime"):
                booked_times.append(time_value.strftime("%H:%M"))
            else:
                booked_times.append(str(time_value)[:5])

        return booked_times

    @staticmethod
    def is_slot_booked(doctor_id, appointment_date, appointment_time):
        existing = db.session.execute(text("""
            SELECT 1
            FROM Appointment
            WHERE DoctorID = :doctor_id
            AND AppointmentDate = :date
            AND AppointmentTime = :time
            AND StatusID != 3
        """), {
            "doctor_id": doctor_id,
            "date": appointment_date,
            "time": appointment_time
        }).fetchone()

        return existing is not None

    @staticmethod
    def book(data, user_id):
        doctor_id = data.get("doctor_id")

        if not doctor_id:
            return False

        # 🔥 نجيب الـ patient الحقيقي بدل 1
        profile = PatientService.get_profile_by_user_id(user_id)
        if not profile:
            return False

        patient_id = profile["PersonID"]

        date_str = data["date"]
        time_str = data.get("time", "00:00")

        if "AM" in time_str or "PM" in time_str:
            dt_format = "%Y-%m-%d %I:%M %p"
        else:
            dt_format = "%Y-%m-%d %H:%M"

        try:
            full_datetime = datetime.strptime(f"{date_str} {time_str}", dt_format)
        except ValueError:
            return False

        appointment_date = full_datetime.date()
        appointment_time = full_datetime.time()

        # منع الحجز المكرر
        if AppointmentService.is_slot_booked(
            doctor_id,
            appointment_date,
            appointment_time
        ):
            return False

        db.session.execute(text("""
            INSERT INTO Appointment
            (
                PatientID,
                DoctorID,
                AppointmentDate,
                AppointmentTime,
                StatusID,
                Notes,
                PatientName,
                PatientEmail,
                VisitReason
            )
            VALUES
            (
                :patient_id,
                :doctor_id,
                :date,
                :time,
                :status,
                :notes,
                :name,
                :email,
                :reason
            )
        """), {
            "patient_id": patient_id,  # ✅ الحل هنا
            "doctor_id": doctor_id,
            "date": appointment_date,
            "time": appointment_time,
            "status": 1,
            "notes": data.get("notes"),
            "name": data["name"],
            "email": data["email"],
            "reason": data["reason"]
        })

        db.session.commit()
        return True

    @staticmethod
    def cancel(appointment_id, user_id):
        """Delete an appointment from the database — only if it belongs to the patient."""
        from app.services.patient_service import PatientService
        profile = PatientService.get_profile_by_user_id(user_id)
        if not profile:
            return False, "Patient not found"

        patient_id = profile["PersonID"]

        # Verify ownership before deleting
        appt = db.session.execute(text("""
            SELECT AppointmentID
            FROM Appointment
            WHERE AppointmentID = :appt_id AND PatientID = :patient_id
        """), {"appt_id": appointment_id, "patient_id": patient_id}).fetchone()

        if not appt:
            return False, "Appointment not found"

        try:
            db.session.execute(text("""
                DELETE FROM Appointment
                WHERE AppointmentID = :appt_id AND PatientID = :patient_id
            """), {"appt_id": appointment_id, "patient_id": patient_id})
            db.session.commit()
        except Exception:
            db.session.rollback()
            return False, "Could not delete appointment"

        return True, "Appointment deleted successfully"

    @staticmethod
    def reschedule(appointment_id, user_id, new_date_str, new_time_str):
        """Reschedule an appointment to a new date/time."""
        from app.services.patient_service import PatientService
        profile = PatientService.get_profile_by_user_id(user_id)
        if not profile:
            return False, "Patient not found"

        patient_id = profile["PersonID"]

        # Verify ownership
        appt = db.session.execute(text("""
            SELECT AppointmentID, DoctorID, StatusID
            FROM Appointment
            WHERE AppointmentID = :appt_id AND PatientID = :patient_id
        """), {"appt_id": appointment_id, "patient_id": patient_id}).fetchone()

        if not appt:
            return False, "Appointment not found"

        if appt[2] == 3:
            return False, "Cannot reschedule a cancelled appointment"

        doctor_id = appt[1]

        if "AM" in new_time_str or "PM" in new_time_str:
            dt_format = "%Y-%m-%d %I:%M %p"
        else:
            dt_format = "%Y-%m-%d %H:%M"

        try:
            full_datetime = datetime.strptime(f"{new_date_str} {new_time_str}", dt_format)
        except ValueError:
            return False, "Invalid date or time format"

        new_date = full_datetime.date()
        new_time = full_datetime.time()

        # Check that the new slot is not already taken by another appointment
        conflict = db.session.execute(text("""
            SELECT 1 FROM Appointment
            WHERE DoctorID = :doctor_id
              AND AppointmentDate = :date
              AND AppointmentTime = :time
              AND StatusID != 3
              AND AppointmentID != :appt_id
        """), {"doctor_id": doctor_id, "date": new_date, "time": new_time, "appt_id": appointment_id}).fetchone()

        if conflict:
            return False, "This slot is already booked. Please choose another time."

        try:
            db.session.execute(text("""
                UPDATE Appointment
                SET AppointmentDate = :date,
                    AppointmentTime = :time,
                    StatusID = 1
                WHERE AppointmentID = :appt_id AND PatientID = :patient_id
            """), {"date": new_date, "time": new_time, "appt_id": appointment_id, "patient_id": patient_id})
            db.session.commit()
        except Exception:
            db.session.rollback()
            return False, "Could not reschedule appointment"

        return True, "Appointment rescheduled successfully"