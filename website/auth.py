from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["Get","Post"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category="sucess")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("password incorrect", category="error")

    return render_template("login.html",user=current_user)


@auth.route("/sign-up", methods=["Get" ,"Post"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        user_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash("Email already in use", category="error")
        if user_exists:
            flash("Username already in use", category="error")
        elif password1 != password2:
            flash("Passwords dont match", category="error")
        elif len(username) < 2:
            flash("Username to short at least 2 characters needed", category="error")
        elif len(password1) < 6:
            flash("Password to short at least 6 characters needed", category="error")
        elif "@" not in email or len(email) < 4:
            flash("not a viable email", category="error")
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash("User created")
            return redirect(url_for("views.home"))

    return render_template("signup.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("loged out sucesfully",category="sucess")
    return redirect(url_for("views.home")) #references the function home in views