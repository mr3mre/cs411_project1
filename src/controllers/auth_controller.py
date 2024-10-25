from flask import session, redirect, render_template, flash, Request
from src.services.auth_service import AuthService
from src.config.settings import config

class AuthController:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def login(self, request: Request):
        if request.method == "GET":
            usernames = self.auth_service.get_usernames() if config.USERSLISTLOGIN else []
            return render_template("login.html", config=config, usernames=usernames)

        user_name = request.form.get("user_name", "")
        password = request.form.get("password", "")

        success, user, message = self.auth_service.authenticate(user_name, password)
        
        if success:
            session["id"] = user.user_name
            session["logged_in"] = True
            return redirect("/dashboard")
        
        flash(message, "alert alert-warning" if "blank" in message.lower() else "alert alert-danger")
        return redirect("/login")

    def logout(self):
        session.clear()
        return redirect("/login")

