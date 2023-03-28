import requests

job_post_data = {
    "username": "test1",
    "passwd": "test2",
    "text": "please show me the right msg."
}

job_get_data = {
    "id": 123456
}

data = requests.post("http://172.16.0.133:5000/job", json=job_post_data)

print(data.json())


data = requests.get("http://172.16.0.133:5000/job", json=job_get_data)

print(data.json())