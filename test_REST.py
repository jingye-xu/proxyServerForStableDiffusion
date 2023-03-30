import requests
url = "http://172.16.0.133:5000"
job_post_data = {
    "username": "Gabriel",
    "passwd": "stupidsimple",
    "text": "show me the right msg."
}

job_get_data = {
    "id": 123456
}

login_test = {
    "username": "hello",
    "passwd": "test1"
}

# data = requests.post("http://172.16.0.133:5000/job", json=job_post_data)

# print(data.json())


# data = requests.get("http://172.16.0.133:5000/job", json=job_get_data)

# print(data.json())

data = requests.post(url+"/job", json=job_post_data)
print(data.json())
print(data.json()["status"])