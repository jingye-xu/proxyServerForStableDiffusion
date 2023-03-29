from flask import Flask, render_template, request, url_for, redirect, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import pandas as pd
from os.path import exists
import sys
import local_config
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import random


credentials = {}
job_queue = []
job_complete = {}


app = Flask(__name__)


def validation(name, pw):
    if name in credentials:
        if credentials[name] == pw:
            return True
        return False
    else:
        return False


def sign_check(name, pw):
    if name in credentials:
        return False
    else:
        credentials[name] = pw
        return True


@app.route('/', methods=['GET'])
# used to check if the server is accessible
def index():
    data = {"test": 1}
    return jsonify(data)


@app.route('/job', methods=['GET', 'POST'])
def job():
    data = request.json
    # post method
    if request.method == "POST":
        username = data.get("username")
        passwd = data.get("passwd")
        text = data.get("text")
        if validation(username, passwd):
            job_id = random.getrandbits(64)

            # put job into a queue
            job_queue.append((job_id, text))

            # send info back to client
            reply = {"status": 0, "id": job_id}
            return jsonify(reply)
        else:
            reply = {"status": 1, "id": 0}
            return jsonify(reply)
    else:
        job_id = data.get("id")

        # search results from the complete queue
        if job_id in job_complete:
            img = job_complete[job_id]
            reply = {"id": job_id, "img": img}
            return jsonify(reply)
        else:
            reply = {"id": job_id, "img": None}
            return jsonify(reply)


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get("username")
    passwd = data.get("passwd")
    if sign_check(username, passwd):
        reply = {"status": 0}
        return jsonify(reply)
    else:
        reply = {"status": 1}
        return jsonify(reply)


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    passwd = data.get("passwd")
    if validation(username, passwd):
        reply = {"status": 0}
        return jsonify(reply)
    else:
        reply = {"status": 1}
        return jsonify(reply)


if __name__ == "__main__":
    
    app.run(debug=True, host="0.0.0.0", port=int(local_config.webserver_port))
