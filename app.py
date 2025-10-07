from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Stack2764@localhost/Tracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(100), nullable = False)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user:
            if user.password == password:
                return redirect(url_for('mainpage'))

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user:
            msg = "⚠️ User account already exists. Please log in instead."
            return render_template('signup.html', msg=msg)
        else:
            new_user = User(first_name=fname,
                        last_name=lname,
                        email=email,
                        password=password)

            db.session.add(new_user)
            db.session.commit()

        return f"<h2>Welcome, {fname} {lname}!</h2><p>Your account has been saved!</p>"

    return render_template('signup.html')

@app.route('/mainpage')
def mainpage():
    return f"<h1> Welcome back!! </h1>"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)