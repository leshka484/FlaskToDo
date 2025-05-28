from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from app.crud import check_password, create_user, read_user
from app.extensions import Session
from app.forms import LoginForm, RegisterForm

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        create_user(Session, name, password)
        flash("Регистрация прошла успешно!", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = read_user(Session, form.name.data)
        if user and check_password(user, form.password.data):
            login_user(user)
            flash("Вход выполнен успешно!", "success")
            return redirect(url_for("index"))
    return render_template("login.html", form=form)


@auth_bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for("index"))
