from flask import Blueprint, render_template
from app.services.specialty_service import SpecialtyService

specialty_bp = Blueprint("specialty", __name__)

@specialty_bp.route("/specialties")
def specialties():
    specialties = SpecialtyService.get_all_specialties()
    return render_template("specialties.html", specialties=specialties)