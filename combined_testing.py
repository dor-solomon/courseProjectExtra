import requests
from db_connector import get_user, config, cmd_args
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.chrome import ChromeType
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service as Servicef
from selenium.webdriver.firefox.options import Options as Optionsf
from selenium.webdriver.common.by import By
from sys import argv
from os import path

cmd_args(argv)

user_id = 4
config = config()
user_name = config[2]
link = config[0]
browser = config[1]

chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
firefox_service = Servicef(GeckoDriverManager().install(), log_path=path.devnull)

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

firefox_options = Optionsf()
for option in options:
    firefox_options.add_argument(option)

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

    if browser == "chrome":
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    elif browser == "firefox":
        driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
    driver.implicitly_wait(2)
    driver.get(f"http://127.0.0.1:5001/users/get_user_data/{user_id}")
    user_name = driver.find_element(By.ID, "user")
    print(user_name.text)
except:
    raise Exception("test failed")

driver.quit()
