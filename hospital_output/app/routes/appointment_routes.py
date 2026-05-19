from flask import Blueprint, request, redirect, url_for, session, jsonify, flash
from app.services.appointment_service import AppointmentService

appointment_bp = Blueprint("appointment", __name__)

@appointment_bp.route("/get_booked_slots", methods=["GET"])
def get_booked_slots():
    doctor_id = request.args.get("doctor_id")
    # Sanitize doctor_id
    if doctor_id and '?' in str(doctor_id):
        doctor_id = str(doctor_id).split('?')[0]
        
    date_str = request.args.get("date") # Expected YYYY-MM-DD
    
    if not date_str or not doctor_id:
        return jsonify([])
    
    # You might want to validate date_str format here
    slots = AppointmentService.get_booked_slots(doctor_id, date_str)
    return jsonify(slots)

@appointment_bp.route("/book_appointment", methods=["POST"])
def book_appointment():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    doctor_id = request.form.get("doctor_id")
    # Sanitize doctor_id just in case
    if doctor_id and '?' in str(doctor_id):
        doctor_id = str(doctor_id).split('?')[0]

    if not doctor_id:
         flash("Please select a doctor.", "error")
         return redirect(url_for("doctor.doctors_page"))

    data = {
        "name": request.form["full_name"],
        "email": request.form["email"],
        "reason": request.form["reason"],
        "date": request.form["date"],
        "time": request.form["time"],
        "doctor_id": doctor_id # Get the doctor ID
    }

    user_id = session.get("user_id")
    success = AppointmentService.book(data, user_id)
    
    if not success:
        flash("This slot is already booked. Please choose another one.", "error")
        return redirect(url_for("doctor.doctors_page")) # Or wherever the booking originated

    flash("Appointment booked successfully!", "success")
    return redirect(url_for("doctor.doctors_page"))


@appointment_bp.route("/cancel_appointment/<int:appointment_id>", methods=["POST"])
def cancel_appointment(appointment_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    success, message = AppointmentService.cancel(appointment_id, user_id)

    if success:
        flash(message, "success")
    else:
        flash(message, "error")

    return redirect(url_for("patient.patient_profile"))


@appointment_bp.route("/reschedule_appointment/<int:appointment_id>", methods=["POST"])
def reschedule_appointment(appointment_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    new_date = request.form.get("new_date")
    new_time = request.form.get("new_time")

    if not new_date or not new_time:
        flash("Please provide a new date and time.", "error")
        return redirect(url_for("patient.patient_profile"))

    success, message = AppointmentService.reschedule(appointment_id, user_id, new_date, new_time)

    if success:
        flash(message, "success")
    else:
        flash(message, "error")

    return redirect(url_for("patient.patient_profile"))