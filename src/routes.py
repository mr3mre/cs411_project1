from flask import Blueprint, request, render_template, session, redirect, abort, flash
from pip._vendor import cachecontrol
import json
import re
from src.controllers.auth_controller import AuthController
from src.services.auth_service import AuthService
from src.repositories.user_repository import UserRepository

# Setup dependencies
user_repository = UserRepository("users.json")
auth_service = AuthService(user_repository)
auth_controller = AuthController(auth_service)

bp = Blueprint("routes", __name__)

# Login Page
@bp.route("/")
def index():
    return redirect("/login")

@bp.route("/login", methods=["GET", "POST"])
def login():
    return auth_controller.login(request)

# Logout
@bp.route("/logout", methods=["POST"])
def logout():
    return auth_controller.logout()

# Protected page
@bp.route("/dashboard", methods=["GET"])
def dashboard():
    if "logged_in" not in session or session["logged_in"] != True:
        return abort(401)
    
    # Get user from repository using session id
    user = user_repository.get_user_by_username(session.get("id"))
    if not user:
        session.clear()
        return redirect("/login")
        
    return render_template("dashboard.html", user=user)
