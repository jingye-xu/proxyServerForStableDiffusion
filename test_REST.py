import requests
import base64


def base64toimg(input: str, filename: str="imageToSave.png"):
    input = input.encode('utf-8')
    print(input)
    with open(filename, "wb") as f:
        f.write(base64.decodebytes(input))

url = "http://172.16.0.133:5000"
job_post_data = {
    "username": "Gabriel",
    "passwd": "stupidsimple",
    "text": "show me the right msg."
}

job_get_data = {
    "username": "Gabriel",
    "passwd": "stupidsimple",
    "id": 29604
}

login_test = {
    "username": "hello",
    "passwd": "test1"
}


data = requests.post(url+"/job_get", json=job_get_data)
# print(data.json())
base64toimg(data.json()["img"])