from flask import Flask, render_template, request, url_for, redirect, jsonify
from os.path import exists
import sys
import local_config
import random
import collections


credentials = {}
job_queue = []
job_complete = collections.defaultdict(list)
queue_hard_username = "gpu"
queue_hard_passwd = "is private"
random_number_bit_width = 16

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
    data = {"test": 0}
    return jsonify(data)


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    print(data)
    print(type(data))
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
    print(data)
    print(type(data))
    username = data.get("username")
    passwd = data.get("passwd")
    if validation(username, passwd):
        reply = {"status": 0}
        return jsonify(reply)
    else:
        reply = {"status": 1}
        return jsonify(reply)


@app.route('/job', methods=['GET', 'POST'])
def job():
    data = request.json
    print(data)
    print(type(data))
    username = data.get("username")
    passwd = data.get("passwd")
    
    if not validation(username, passwd):
        reply = {"status": 1, "id": 0, "img": ""}
        return jsonify(reply)
    
    # post method
    if request.method == "POST":
        text = data.get("text")

        job_id = random.getrandbits(random_number_bit_width)
        print(text)

        # put job into a queue
        job_queue.append((job_id, text))
        print(job_queue)

        # send info back to client
        reply = {"status": 0, "id": job_id, "img": ""}
        return jsonify(reply)
    else:
        job_id = data.get("id")
        # search results from the complete queue
        if len(job_complete[job_id]):
            img = job_complete[job_id].pop(0)
            reply = {"status": 2, "id": job_id, "img": img}
            return jsonify(reply)
        else:
            reply = {"status": 3, "id": job_id, "img": ""}
            return jsonify(reply)


@app.route('/job_get', methods=['POST'])
def job_get():
    data = request.json
    print(data)
    username = data.get("username")
    passwd = data.get("passwd")
    
    if not validation(username, passwd):
        reply = {"status": 1, "id": 0, "img": ""}
        return jsonify(reply)
    
    job_id = data.get("id")
    # search results from the complete queue
    if len(job_complete[job_id]):
        img = job_complete[job_id].pop(0)
        reply = {"status": 2, "id": job_id, "img": img}
        return jsonify(reply)
    else:
        reply = {"status": 3, "id": job_id, "img": ""}
        return jsonify(reply)


@app.route('/queue', methods=['GET', 'POST'])
def queue():
    data = request.json
    # print(data)
    # print(type(data))
    username = data.get("username")
    passwd = data.get("passwd")
    
    # hard queue username and passwd validation
    if username != queue_hard_username or passwd != queue_hard_passwd:
        reply = {"status": 1, "id": 0, "text": ""}
        return jsonify(reply)

    if request.method == "GET":
        if not len(job_queue):
            reply = {"status": 1, "id": 0, "text": ""}
            return jsonify(reply)

        job = job_queue.pop(0)
        print(job)
        reply = {"status": 0, "id": job[0], "text": job[1]}
        return jsonify(reply)

    elif request.method == "POST":
        job_id = data.get("id")
        img = data.get("img")
        print(job_id)
        # print(img)
        job_complete[job_id].append(img)
        print("length changed to: ")
        print(len(job_complete[job_id]))
        reply = {"status": 2, "id": job_id, "text": ""}
        return jsonify(reply)
    else:
        reply = {"status": 3, "id": 0, "text": ""}
        return jsonify(reply)


if __name__ == "__main__":
    
    app.run(debug=False, host="0.0.0.0", port=int(local_config.webserver_port))
