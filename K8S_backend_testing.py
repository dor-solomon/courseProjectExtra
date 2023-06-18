import requests
from db_connector import config, cmd_args
from sys import argv

cmd_args(argv)
user_id = 4
config = config()
user_name = config[2]

# read url from k8s_url.txt
with open("k8s_url.txt", "r") as url:
    k8s = (url.read().rstrip())

link = k8s + "/users/"

try:
    requests.post(f'{link}{user_id}', json={"user_name":f"{user_name}"})
except:
    raise Exception("test failed")
res = requests.get(f'{link}{user_id}')
resp = res.json()
if resp.get("user_name") == f"{user_name}" and res.status_code == 200:
    print(resp.get("user_name"), res.status_code)
else:
    raise Exception("test failed")
