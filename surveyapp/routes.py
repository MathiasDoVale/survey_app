from flask import Flask, render_template, request, session, logging, url_for, redirect, flash
from surveyapp.models import User
from surveyapp import app, db, login_manager, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from surveyapp.forms import RegistrationForm, LoginForm
import os

# Chequeo si existe la bd
if not os.path.isfile('surveyapp/test.db'):
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id)

@app.route("/")
@app.route("/home")
@login_required
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.email.data}!', 'success')
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html", form=form)

@app.route("/login",methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user is not None and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)
            db.session.add(user)
            db.session.commit()
            flash('You have been logged in!', 'success')
            return redirect(url_for("home"))
    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for("login"))