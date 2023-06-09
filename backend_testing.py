import requests
from sys import argv
from db_connector import DBfunc

args = argv
db = DBfunc(args[1], args[1], args[2], args[3])

user_id = 4
config = db.config()
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

if db.get_user(user_id) == user_name:
    print(db.get_user(user_id))
else:
    raise Exception("test failed")
