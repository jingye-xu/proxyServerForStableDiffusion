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


app = Flask(__name__)


def validation(name, pw):
    return True


def sign(name, pw):
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

            # TODO: put job into a queue

            # send info back to client
            reply = {"status": 0, "id": job_id}
            return jsonify(reply)
        else:
            reply = {"status": 1, "id": 0}
            return jsonify(reply)
    else:
        job_id = data.get("id")

        # TODO: search results from the complete queue
        
        reply = {"id": job_id, "img": "img"}
        return jsonify(reply)


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get("username")
    passwd = data.get("passwd")
    if sign(username, passwd):
        reply = {"status": 0}
        return jsonify(reply)
    else:
        reply = {"status": 1}
        return jsonify(reply)


if __name__ == "__main__":
    
    app.run(debug=True, host="0.0.0.0", port=int(local_config.webserver_port))
