from app.models.Speciality import Specialties


class SpecialtyService:

    @staticmethod
    def get_all_specialties():
        return Specialties.query.all()