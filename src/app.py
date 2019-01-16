'''
This is the app to add contact list
'''
import logging
import os

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from logging.config import dictConfig
from flask.logging import default_handler

from auth import *

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
RESULT_COUNT = 10

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///flask_app.db')

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)
LOGGER = logging.getLogger()
LOGGER.addHandler(default_handler)

class User(db.Model):
    email = db.Column(db.String(60), primary_key=True)
    name = db.Column(db.String(20))
    city = db.Column(db.String(20))

    def __init__(self, name, email, city):
        self.name = name
        self.email = email
        self.city = city


@app.route('/', methods=['GET'])
@auth.login_required
def index():
    username = auth.username()
    return render_template('home.html')

@app.route('/delete_user', methods=['DELETE'])
@auth.login_required
def delete_user():
    email = request.args.get('email')
    if email:
        _user = User.query.filter_by(email=email).first()
        if _user:
            db.session.delete(_user)
            db.session.commit()
            return "Deleted user successfully"
        else:
            return "No such user exist"

    return "Missing email in request, discarding"


@app.route('/update_user', methods=['PUT'])
@auth.login_required
def update_user():
    _email = request.args.get('email')
    if not _email:
      return "email is missing in request body"

    _name = request.args.get('name')
    _city = request.args.get('city')
    _user = User.query.filter_by(email=_email).first()

    if _user:
        if _name:
            _user.name = _name
        if _city:
            _user.city = _city
        db.session.commit()
        msg = "Updated User {} successfully".format(_name)
        LOGGER.info(msg)
        return msg
    else:
        return "Email doesn't exist in db"


@app.route('/add_user', methods=['POST'])
@auth.login_required
def add_user():
    _email = request.args.get('email')
    _name = request.args.get('name')
    _city = request.args.get('city')

    if _name and _email and _city:
        user = User.query.filter_by(email=_email).first()
        if user:
            return "email id already exist, please use something else"

        _user = User(_name, _email, _city)
        db.session.add(_user)
        db.session.commit()
        msg = "Added user : {}".format(_name)
        LOGGER.info(msg)
        return msg
    else:
        return "Missing one of these arguments, name = [{}], email = [{}], city = [{}]".format(_name, _email, _city)


@app.route('/search_by_name', methods=['GET'])
def search_by_name():
    _name = request.args.get('name')
    if _name:
        LOGGER.info("Searcing by name : %s", _name)
        user = User.query.filter(User.name == _name).limit(RESULT_COUNT).all()
        return render_template('users.html', users=user)
    elif _name is None:
        return "Missing argument _name"
    else:
        return "Need a value for _name"


@app.route('/search_by_email', methods=['GET'])
def search_by_email():
    _email = request.args.get('email')
    if _email:
        LOGGER.info("Searcing by email : %s", _email)
        u = User.query.filter(User.email == _email).limit(RESULT_COUNT).all()
        return render_template('users.html', users=u)
    elif _email is None:
        return "Missing argument _email"
    else:
        return "Need a value for _email"


if __name__ == '__main__':
    LOGGER.info("Starting app")
    db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
