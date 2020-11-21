from flask import Flask, render_template, request, session, logging, url_for, redirect, flash
from surveyapp.models import User, Survey, Question, Choice
from surveyapp import app, db, login_manager, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from surveyapp.forms import RegistrationForm, LoginForm, SurveyForm, QuestionForm
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
    """Home page"""
    return render_template("home.html")

@app.route("/register", methods=["GET","POST"])
def register():
    """Register a user."""
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
    """Login the current user."""
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


@app.route("/new_survey",methods=["GET", "POST"])
@login_required
def new_survey():
    """Creates a new survey with at least one question."""
    form = SurveyForm()
    if form.validate_on_submit():
        user = current_user
        # Survey creation
        new_survey = Survey(title=form.title.data, user_id=user.email)
        db.session.add(new_survey)
        db.session.commit()
        # Question creation
        new_question = Question(question_text=form.question.data, survey_id=new_survey.id)
        db.session.add(new_question)
        db.session.commit()
        # Choices creation (minimum 2)
        new_choice_1 = Choice(choice_text=form.option_1.data, question_id=new_question.id, votes=0)
        db.session.add(new_choice_1)
        db.session.commit()

        new_choice_2 = Choice(choice_text=form.option_2.data, question_id=new_question.id, votes=0)
        db.session.add(new_choice_2)
        db.session.commit()

        # Checking if choice 3 and 4 are empty
        if not form.option_3.data == '':
            new_choice_3 = Choice(choice_text=form.option_3.data, question_id=new_question.id, votes=0)
            db.session.add(new_choice_3)
            db.session.commit()

        if not form.option_4.data == '':
            new_choice_4 = Choice(choice_text=form.option_4.data, question_id=new_question.id, votes=0)
            db.session.add(new_choice_4)
            db.session.commit()

        return redirect(url_for("add_question", survey_id=new_survey.id))

    return render_template("new_survey.html", form=form)

@app.route('/add_question/<string:survey_id>', methods=['GET', 'POST'])
@login_required
def add_question(survey_id):
    """Add a new question to the survey."""

    form = QuestionForm()
    if form.validate_on_submit():
        # Question creation
        new_question = Question(question_text=form.question.data, survey_id=survey_id)
        db.session.add(new_question)
        db.session.commit()
        # Choices creation (minimum 2)
        new_choice_1 = Choice(choice_text=form.option_1.data, question_id=new_question.id, votes=0)
        db.session.add(new_choice_1)
        db.session.commit()

        new_choice_2 = Choice(choice_text=form.option_2.data, question_id=new_question.id, votes=0)
        db.session.add(new_choice_2)
        db.session.commit()

        # Checking if choice 3 and 4 are empty
        if not form.option_3.data == '':
            new_choice_3 = Choice(choice_text=form.option_3.data, question_id=new_question.id, votes=0)
            db.session.add(new_choice_3)
            db.session.commit()

        if not form.option_4.data == '':
            new_choice_4 = Choice(choice_text=form.option_4.data, question_id=new_question.id, votes=0)
            db.session.add(new_choice_4)
            db.session.commit()

        return redirect(url_for("add_question", survey_id=survey_id))


    return render_template(("/add_question.html"), form=form)

