from flask import Blueprint, request, redirect, url_for, render_template, session
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    return AuthService.signup()

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    return AuthService.login()

@auth_bp.route("/logout")
def logout():
    return AuthService.logout()