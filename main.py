from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os
from dotenv import load_dotenv

load_dotenv(".env")  # loads the environment file

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()  # creates an instance of the Login Manager class, contains the code that lets your
# application and Flask-Login work together, such as how to load a user from an ID, where to send users when they
# need to log in

login_manager.init_app(app)  # configures our app for login


@login_manager.user_loader
def load_user(user_id):  # function for reloading the user from its user id
    return User.query.get(int(user_id))


# CREATE TABLE IN DB
class User(UserMixin, db.Model):  # inheriting from both UserMixin and db.Model
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
#Line below only required once, when creating DB. 
# db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # if user is already authenticated
        return redirect(url_for('secrets'))
    if request.method == "POST":
        user_name = request.form['name']
        user_email = request.form['email']
        if User.query.filter_by(email=user_email).first():
            flash("You already signed up with that email. Log in instead !")
            return redirect(url_for('login'))
        user_password = request.form['password']
        hashed_password = generate_password_hash(password=user_password, method='pbkdf2:sha256', salt_length=8)
        new_user = User(email=user_email, password=hashed_password, name=user_name)
        db.session.add(new_user)
        db.session.commit()
        return render_template('secrets.html', name=user_name)

    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # if user is already authenticated
        return redirect(url_for('secrets'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first() # finds the user in the database via the email
        if not user:
            # user doesn't exist
            flash("That email does not exist, please try again.")
        elif not check_password_hash(pwhash=user.password,password=password):
            # password is not correct
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))

        else:  # user and password are both correct
            login_user(user)  # logs the user in
            return redirect(url_for('secrets'))

    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html")


@app.route('/logout')
def logout():
    logout_user()  # will log out the user by ending the user session
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    directory = 'static/files'  # directory path in the project, then we hardcode the file name in send_from_directory
    # we turn as_attachment to false in order not for the file to download but to open inside the browser
    return send_from_directory(directory=directory, filename="cheat_sheet.pdf", as_attachment=False)




if __name__ == "__main__":
    app.run(debug=True)
