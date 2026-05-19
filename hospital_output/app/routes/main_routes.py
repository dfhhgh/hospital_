from flask import Blueprint, render_template, redirect, url_for, session
from app.services.doctor_service import DoctorService

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return redirect(url_for("auth.login"))

@main_bp.route("/home")
def home_page():
    doctors = DoctorService.get_doctors()[:4] # Display top 4 doctors
    return render_template("index.html", doctors=doctors)

@main_bp.route("/about")
def about_page():
    return render_template("about.html")

@main_bp.route("/contact")
def contact_page():
    return render_template("contact.html")
@main_bp.route("/departments")
def departments_page():
    return render_template("specialties.html")

@main_bp.route("/appointment")
def appointment_page():
    from flask import request
    doctor_id = request.args.get("doctor_id")
    
    # Sanitize doctor_id just in case of weird URLs
    if doctor_id and '?' in str(doctor_id):
        doctor_id = str(doctor_id).split('?')[0]
        
    doctor = None
    if doctor_id:
        # Check if it's a valid integer before querying
        try:
            int_id = int(doctor_id)
            doctor = DoctorService.get_doctor(int_id)
        except ValueError:
            pass # Invalid ID format, ignore
        
    return render_template("appointment.html", doctor=doctor)