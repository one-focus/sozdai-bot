import os

import requests
from selenium import webdriver

# URL = 'https://algeria.blsspainvisa.com/english/book_appointment.php'
URL = 'https://app.bookitit.com/en/hosteds/widgetdefault/2dfa8d208fa12dcbe904341150d0c10ce'
IS_MONITORING = False


def monitor():
    r = requests.get(URL)
    print(str(r.content))
    if str(r.content) == "b''":
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