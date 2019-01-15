import os
import hashlib
import logging

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from logging.config import dictConfig
from flask.logging import default_handler
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

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

PASSWORD =  os.environ['password']
USERNAME = os.environ['username']

LOGGER = logging.getLogger()
LOGGER.addHandler(default_handler)

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)

class User(db.Model):
  email = db.Column(db.String(60), primary_key=True)
  name = db.Column(db.String(20))
  city = db.Column(db.String(20))  

  def __init__(self, name, email, city):
    self.name = name
    self.email = email
    self.city = city
    

@auth.get_password
def get_pw(username):
    has_pwd  = PASSWORD
    return has_pwd

@auth.hash_password
def hash_pw(password):
    return hashlib.md5(password.encode()).hexdigest()

@auth.verify_password
def verify_password(username, password):
    if hash_pw(password) == get_pw(username) and username == USERNAME:
      return True

    return False

@app.route('/', methods=['GET'])
@auth.login_required
def index():
  username = auth.username()
  return "{}, Welcome to contact page.\nPlease use 'add_user/update_user/delete_user/search_by_email/search_by_name' endpoints ".format(username.lower())

@app.route('/delete_user', methods=['DELETE'])
@auth.login_required
def delete_user():
    email = request.args.get('email')
    print(request.args)
    if email:
      _user = User.query.filter_by(email=email).first()
      if _user:
        db.session.delete(_user)
        db.session.commit()
        return "Deleted user"
      else:
        return "No such user"

    return "Missing email"

@app.route('/update_user', methods=['PUT'])
@auth.login_required
def update_user():
    _email = request.args['email']
    _name =  request.args.get('name')
    _city = request.args.get('city')
    _user = User.query.filter_by(email=_email).first()
    
    if _user : 
      if _name:
        _user.name = _name
      if _city:
        _user.city = _city
      db.session.commit()
      return "Updated User {}".format(_name)
    else:
      return "Email doesn't exist"

@app.route('/add_user', methods=['POST'])
@auth.login_required
def add_user():
    _email = request.args.get('email')
    _name =  request.args.get('name')
    _city = request.args.get('city')

    if _name and _email and _city:
  	  user = User.query.filter_by(email=_email).first()
  	  if user:
  		  return "email id already exist, please use something else"

      _user = User(_name, _email, _city)
      db.session.add(_user)
      db.session.commit()
      return "Added user : {}".format(_name)
    else:
      return "Missing one of argument, name = [{}], email = [{}], city = [{}]".format(_name, _email, _city)

@app.route('/search_by_name', methods=['GET'])
def search_by_name():
    _name = request.args.get('name')
    if _name:
      u = User.query.filter(User.name==_name).limit(RESULT_COUNT).all()
      print(u)
      return render_template('users.html', users = u)
    elif _name is None:
      return "Missing argument _name"
    else:
      return "Need a value for _name"

@app.route('/search_by_email', methods=['GET'])
def search_by_email():
    _email = request.args.get('email')
    if _email:
      u = User.query.filter(User.email == _email).limit(RESULT_COUNT).all()
      print(u)
      return render_template('users.html', users = u)
    elif _email is None:
      return "Missing argument _email"
    else:
      return "Need a value for _email"

if __name__ == '__main__':
  LOGGER.info("Starting app")
  db.create_all()
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
