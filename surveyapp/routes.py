from flask import Flask, render_template, request, session, logging, url_for, redirect, flash
from surveyapp.models import User
from surveyapp import app, db
from flask_login import LoginManager, login_required, login_user, logout_user, login_manager, current_user
from surveyapp.forms import RegistrationForm, LoginForm

db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.email.data}!', 'success')
        email = request.form.get("email")
        password = request.form.get("password")
        new_user = User(email=email, password=password)
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
        user = User.query.filter_by(email=email, password=password).first()
        if user is not None:
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