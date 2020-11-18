from flask import Flask, render_template, request, session, logging, url_for, redirect, flash
from flask_sqlalchemy  import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user, login_manager, current_user
from models import User


# SETTINGS
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id)

@app.route("/")
@login_required
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        # Valido misma password
        if password == confirm:
            new_user = User(email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            flash("Password does not match","danger")
            return render_template("register.html")

    return render_template("register.html")

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email, password=password).first()
        if user is not None:
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            return redirect(url_for("home"))
    return render_template("login.html")

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


if __name__ == "__main__":
    app.debug = True
    db.create_all()
    app.secret_key = "abc123"
    app.run()