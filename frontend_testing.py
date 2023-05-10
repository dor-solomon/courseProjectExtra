from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service as Servicef
from selenium.webdriver.common.by import By
from db_connector import config

user_id = 4
config = config()
browser = config[1]

try:
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
