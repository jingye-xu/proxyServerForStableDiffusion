import requests
import base64
import time


def base64toimg(input: str, filename: str="image.png"):
    input = input.encode('utf-8')
    print(input)
    with open(filename, "wb") as f:
        f.write(base64.decodebytes(input))

url = "http://172.16.0.133:5000"
job_post_data = {
    "username": "Gabriel",
    "passwd": "stupidsimple",
    "text": "teemo."
}

job_get_data = {
    "username": "Gabriel",
    "passwd": "stupidsimple",
    "id": 29604
}

login_test = {
    "username": "Gabriel",
    "passwd": "stupidsimple"
}

# signup
data = requests.post(url+"/signup", json=login_test)

time.sleep(2)

# job post
data = requests.post(url+"/job", json=job_post_data)
job_id = data.json()["id"]
print(f"job id: {job_id}")

job_get_data["id"] = job_id

while True:
    time.sleep(5)
    data = requests.get(url+"/job", json=job_get_data)
    if data.json()["status"] == 2:
        break
    print("still waiting results, wait another 5 seconds")

print("job finished and fetched")
# print(data.json())
base64toimg(data.json()["img"])
print("job saved to img")