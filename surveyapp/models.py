from surveyapp import db

class User(db.Model):
    """User capable to creates surveys.

    :param str email: email of the user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'user'

    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String(80))
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

class Survey(db.Model):
    """Survey created by a user.

    :param str title: title of the survey
    :param str user_id: user who creates the survey
    :param date createdate: date when survey was created
    """
    __tablename__ = 'survey'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.String(80), db.ForeignKey('user.email'), nullable=False)
    created_date = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, title, user_id):
        self.title = title
        self.user_id = user_id

class Question(db.Model):
    """Question can be created on a Survey

    :param str question_text: text of the question
    :param str survey_id: survey of the question
    :param date createdate: date when survey was created
    """
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(80), nullable=False)
    survey_id = db.Column(db.String(80), db.ForeignKey('survey.id'), nullable=False)
    choices = db.relationship('Choice', backref='choice', lazy=True)

    def __init__(self, question_text, survey_id):
        self.question_text = question_text
        self.survey_id = survey_id

class Choice(db.Model):
    """Choice can be created on a question

    :param str choice_text: text of the choice
    :param str question_id: question of the choice
    :param int votes: number of votes of the option
    """
    __tablename__ = 'choice'

    id = db.Column(db.Integer, primary_key=True)
    choice_text = db.Column(db.String(80), nullable=False)
    question_id = db.Column(db.String(80), db.ForeignKey('question.id'), nullable=False)
    votes = db.Column(db.Integer, default=0)

    def __init__(self, choice_text, question_id, votes):
        self.choice_text = choice_text
        self.question_id = question_id
        self.votes = votes

    def vote(self):
        self.votes += 1
        
