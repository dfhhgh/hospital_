from flask import Blueprint, render_template, session, redirect, url_for, request

from app.services.patient_service import PatientService

patient_bp = Blueprint("patient", __name__)

@patient_bp.route("/patient")
def patient_page():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template("patient_profile.html")


@patient_bp.route("/patient/profile", methods=["GET", "POST"])
def patient_profile():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    success = None
    error = None

    if request.method == "POST":
        updated, message = PatientService.update_profile(user_id, request.form)
        if updated:
            success = message
        else:
            error = message

    profile = PatientService.get_profile_by_user_id(user_id)
    if not profile:
        return redirect(url_for("main.home_page"))

    appointments = PatientService.get_patient_appointments(user_id)

    return render_template(
        "patient_profile.html",
        profile=profile,
        appointments=appointments,
        success=success,
        error=error,
    )