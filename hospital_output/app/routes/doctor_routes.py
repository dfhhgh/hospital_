from flask import Blueprint, render_template, request, redirect, url_for, session, Response
from app.services.doctor_service import DoctorService

doctor_bp = Blueprint("doctor", __name__)

@doctor_bp.route("/doctors")
def doctors_page():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    specialty = request.args.get("specialty")
    doctors = DoctorService.get_doctors(specialty)

    return render_template("doctors.html", doctors=doctors)


@doctor_bp.route("/doctor_image/<int:id>")
def doctor_image(id):
    image = DoctorService.get_doctor_image(id)
    return Response(image, mimetype="image/jpeg")