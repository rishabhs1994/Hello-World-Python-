from __future__ import division
from mailgun import *
from pagerduty import *
from redis import Redis
import time
from functools import update_wrapper
from models import Base, User
from flask import Flask, jsonify, request, url_for, abort, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import json
from rate_limit import *
from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

engine = create_engine('sqlite:///users.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

rate_limit_object = RateLimit("Rishabh", 10, 300, True)

@auth.verify_password
def verify_password(username, password):
    user = session.query(User).filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True

@app.after_request
def inject_x_rate_headers(response):
    limit = getattr(g, '_view_rate_limit', None)
    if limit and limit.send_x_headers:
        h = response.headers
        h.add('X-RateLimit-Remaining', str(limit.remaining))
        h.add('X-RateLimit-Limit', str(limit.limit))
        h.add('X-RateLimit-Reset', str(limit.reset))
    return response

#curl -i -X POST -H "Content-Type: application/json" -d '{"username":"Rishabh","password":"Rishabh"}' http://localhost:5000/users
@app.route('/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        print "missing arguments"
        abort(400) 
        
    if session.query(User).filter_by(username = username).first() is not None:
        print "existing user"
        user = session.query(User).filter_by(username=username).first()
        return jsonify({'message':'user already exists'}), 200
        
    user = User(username = username)
    user.hash_password(password)
    session.add(user)
    session.commit()
    return jsonify({ 'username': user.username }), 201

#curl -i -X Get http://localhost:5000/api/users/1
@app.route('/api/users/<int:id>')
def get_user(id):
    user = session.query(User).filter_by(id=id).one()
    if not user:
        abort(400)
    return jsonify({'username': user.username})

#Rate Limited on basis of IP Address.
#curl -i -X GET -H "Content-Type: application/json" -d '{"username":"Rishabh","password":"Rishabh"}' http://localhost:5000/api/resource
@app.route('/api/resource')
@rate_limit_object.ratelimit(10, 1)
@auth.login_required
def get_resource():
    return jsonify({ 'data': 'Hello, %s!' % g.user.username })

#Rate Limited on basis of Logged in user.
#curl -u Rishabh:Rishabh -i -X Get http://localhost:5000/home
@app.route('/home')
@auth.login_required
def getPlayers():
    @rate_limit_object.ratelimit(10, 2, 300, g.user.username)
    def gag():
        return jsonify({'message':'You are visiting rate limiting content, %s' \
        %g.user.username})
    return gag()

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

