from flask import Blueprint, render_template, redirect, url_for, request, flash
from .import db
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
auth = Blueprint("auth", __name__)


@auth.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        username_exist = User.query.filter_by(username=username).first()
        email_exist = User.query.filter_by(email=email).first()
        if (email_exist):
            flash("Email already exist!", category="error")
        elif (username_exist):
            flash("This username already exist!", category="error")
        elif (len(username) < 4):
            flash("Your username should atleast be 4 caracters", category="error")
        elif (len(password) < 6):
            flash("Your password should atleast be 6 caracters", category="error")
        elif (len(email) < 4):
            flash("your email is too short!", category="error")
        else:
            new_user = User(username=username, email=email,
                            password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("welcome you've created your account")
            return redirect(url_for("views.dashboard"))
    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.dashboard'))
            else:
                flash("password is incorrect.", category="error")
                return redirect(url_for('views.login'))
        elif email != user:
            flash("Email does not Exist", category="error")
        elif current_user.authenticated and current_user.username == "admin":
            return redirect("/admin/")

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))
