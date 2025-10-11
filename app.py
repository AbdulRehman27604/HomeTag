import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, session


app = Flask(__name__)
app.secret_key = "dfsfscasfvsrvsvasavawev"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Stack2764@localhost/Tracker'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hometag_db_user:hChQAQXkhGsuGxCiZgEOjruFYqF7dBGf@dpg-d3i8vrripnbc73dvqqjg-a/hometag_db'
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hometag_db_user:hChQAQXkhGsuGxCiZgEOjruFYqF7dBGf@dpg-d3i8vrripnbc73dvqqjg-a.oregon-postgres.render.com/hometag_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    email = db.Column(db.String(100), primary_key=True, nullable=False, unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    password = db.Column(db.String(100), nullable=False)

    items = db.relationship('UserItems', backref='user', lazy=True, cascade="all, delete-orphan")


class UserItems(db.Model):
    __tablename__ = 'useritems'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), db.ForeignKey('users.email', ondelete='CASCADE'), nullable=False)
    itemname = db.Column(db.String(100))
    location = db.Column(db.String(100))
    coordinates = db.Column(db.String(100))
    dates = db.Column(db.String(100))
    available = db.Column(db.String(50))



@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user:
            if user.password == password:
                session['user'] = user.email
                session.permanent = True
                return redirect(url_for('mainpage'))
            else:
                msg = "❌ Incorrect password."
                return render_template('login.html', msg=msg)
        else:
            msg = "⚠️ Account not found. Please sign up."
            return render_template('login.html', msg=msg)

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
            return redirect(url_for('mainpage'))

        return f"<h2>Welcome, {fname} {lname}!</h2><p>Your account has been saved!</p>"

    return render_template('signup.html')

from datetime import datetime

@app.route('/mainpage', methods=['GET', 'POST'])
def mainpage():
    if 'user' in session:
        user_email = session['user']

        if request.method == 'POST':
            item_name = request.form['ItemName']
            location = request.form['Loc']
            coordinates = request.form['Coordinates']
            available = request.form['available']

            new_item = UserItems(
                email=user_email,
                itemname=item_name,
                location=location,
                coordinates=coordinates,
                available=available,
                dates=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            db.session.add(new_item)
            db.session.commit()

            msg = "✅ Item added successfully!"

            # after inserting, refresh the list
            items = UserItems.query.filter_by(email=user_email).all()
            return render_template('mainpage.html', msg=msg, items=items)

        # GET request → just show existing items
        items = UserItems.query.filter_by(email=user_email).all()
        return render_template('mainpage.html', items=items)

    else:
        return redirect(url_for('login'))


@app.route('/additem')
def additem():
    return render_template('additem.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)