import requests

post_data = {
    "username": "test1",
    "passwd": "test2",
    "text": "please show me the right msg."
}

data = requests.post("http://172.16.0.133:5000/job", json=post_data)

print(data.json())