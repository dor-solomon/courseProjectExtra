import requests
from db_connector import get_user, config

user_id = 4
config = config()
user_name = config[2]
link = config[0]

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

if get_user(user_id) == user_name:
    print(get_user(user_id))
else:
    raise Exception("test failed")