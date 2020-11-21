from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SurveyForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    question = StringField('Question', validators=[DataRequired()])
    option_1 = StringField('Option_1', validators=[DataRequired()])
    option_2 = StringField('Option_2', validators=[DataRequired()])
    option_3 = StringField('Option_3', validators=[])
    option_4 = StringField('Option_4', validators=[])
    add_question_submit = SubmitField('Add Question')

class QuestionForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()])
    option_1 = StringField('Option_1', validators=[DataRequired()])
    option_2 = StringField('Option_2', validators=[DataRequired()])
    option_3 = StringField('Option_3', validators=[])
    option_4 = StringField('Option_4', validators=[])
    add_question_submit = SubmitField('Add Question')