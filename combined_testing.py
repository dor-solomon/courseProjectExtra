import requests
from db_connector import get_user, config
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service as Servicef
from selenium.webdriver.common.by import By

user_id = 4
config = config()
user_name = config[2]
link = config[0]
browser = config[1]

try:
    requests.post(f'{link}{user_id}', json={"user_name":f"{user_name}"})
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

    options = Options()
    options.binary_location = "C:/Chromium Ungoogled/bin/chrome.exe"
    if browser == "chrome":
        driver = webdriver.Chrome(options=options, service=Service("C:/chromedriver.exe"))
    elif browser == "firefox":
        driver = webdriver.Firefox(service=Servicef("C:/geckodriver.exe"))
    driver.implicitly_wait(2)
    driver.get(f"http://127.0.0.1:5001/users/get_user_data/{user_id}")
    user_name = driver.find_element(By.ID, "user")
    print(user_name.text)
except:
    raise Exception("test failed")

driver.quit()
