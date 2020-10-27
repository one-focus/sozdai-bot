import os

import requests
from selenium import webdriver

URL = 'https://algeria.blsspainvisa.com/english/book_appointment.php'


def monitor():
    r = requests.get(URL)
    if "Appointment dates are not available." in str(r.content):
        return None
    else:
        return send_screenshot()


def send_screenshot():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1024,768")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.implicitly_wait(120)
    driver.get(URL)
    try:
        driver.find_element_by_class_name('popup-appCloseIcon').click()
    except Exception:
        pass
    return driver.get_screenshot_as_png()
