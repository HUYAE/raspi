import requests

datas = {
    "line_1": 0,
    "line_2": 1,
    "line_3": 0,
    "manually_time": 0,
    "manually_btn": 0
}

url = "http://localhost:8080/api/control-valve"

response = requests.post(url, json=datas)
