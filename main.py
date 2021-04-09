from flask import Flask, render_template, url_for, redirect, request, flash, session
from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy
import json
import forms

app = Flask(__name__)

app.config['SECRET_KEY'] = 'QUWU7Ax94jCsknrT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# creates a User table in the database with appropriate columns 
class User(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   username = db.Column(db.String(50), unique=True, nullable=False)
   password = db.Column(db.String(50), nullable=False)

   def __repr__(self):
       return f"User('{self.username}')"


with open('presets.json', 'r') as input:
    preset_data = json.load(input)

@app.route('/')
@app.route('/home')
def home(): 
    return render_template('home.html')

@app.route("/presets")
def presets():
    return render_template('presets.html', title='Base Data', preset_data = preset_data)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # create instance of a user with info entered from Registration form
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = forms.LoginForm()

    if request.method == "GET":
        return render_template('login.html', form = form)
        print(User.query.all())
    elif request.method == "POST" and form.validate_on_submit():
        user = request.form['username']
        password = request.form['password']
        user_query = User.query.filter_by(username=user).first()

        if user_query is None:
            flash("Invalid Username", "error")
            return render_template('login.html', form = form)
        elif user_query.password != password:
            flash("Invalid Login", "error")
            return render_template('login.html', form = form)
        
        else:
            session['user'] = user_query.username
            return redirect(url_for('userDashboard'))

    return render_template('login.html', form = form)
    

@app.route('/userDashboard')
def userDashboard():
    if 'user' in session:
        user = session['user']
        return render_template('userDashboard.html', user = user)
    else:
        return redirect(url_for('login'))


# run on debug mode to not re-start server after changes
if __name__ == '__main__':

    app.run(debug = True)
