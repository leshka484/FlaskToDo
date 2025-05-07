from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.extensions import Session
from app.crud import *

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST": 
        name = request.form["name"]
        password = request.form["password"]
        create_user(Session, name, password)
        return redirect(url_for("auth.login"))
    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = read_user(Session, request.form["name"])
        if user and check_password(user, request.form["password"]):
            login_user(user)
            return redirect(url_for("index"))
        flash("Неверные имя пользователя или пароль")
    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
