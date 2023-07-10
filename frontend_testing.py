from sys import argv
from os import path
from selenium import webdriver
from db_connector import DBfunc
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeType
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service as Servicef
from selenium.webdriver.firefox.options import Options as Optionsf

args = argv
db = DBfunc(args[1], args[1], args[2], args[3])

user_id = 4
config = db.config()
browser = config[1]

chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
firefox_service = Servicef(GeckoDriverManager().install(), log_path=path.devnull)

chrome_options = Options()
options = [
    "--headless=new",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

firefox_options = Optionsf()
for option in options:
    firefox_options.add_argument(option)

try:
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
