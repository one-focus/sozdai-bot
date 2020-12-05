import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# URL = 'https://algeria.blsspainvisa.com/english/book_appointment.php'
from selenium.webdriver.support.wait import WebDriverWait

URL = 'http://www.exteriores.gob.es/Embajadas/NUEVADELHI/en/Noticias/Pages/Articulos/20200723_NOT8.aspx'
IS_MONITORING = False


def send_screenshot():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1024,768")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.implicitly_wait(120)
    try:
        driver.find_element_by_class_name('popup-appCloseIcon').click()
    except Exception:
        pass
    return driver.get_screenshot_as_png()


def get_dates():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1024,768")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.implicitly_wait(10)
    print('2')
    driver.get(URL)
    print('3')
    driver.find_element_by_xpath("//div[@class='content contenidoLayout']//p[2]/a").click()
    print('4')
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[-1])
    print('5')
    time.sleep(1)
    print('6')
    WebDriverWait(driver, 60).until(
        EC.invisibility_of_element_located((By.XPATH, '//img[@class="clsBktWidgetDefaultLoading"]')))
    print('7')
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'bktContinue'))).click()
    print('8')
    time.sleep(3)
    print('9')
    driver.find_element_by_xpath("//a[contains(@href, 'bkt550308')]").click()
    print('10')
    time.sleep(5)
    print('11')
    WebDriverWait(driver, 60).until(
        EC.invisibility_of_element_located((By.XPATH, '//div[@class="clsDivBktWidgetDefaultLoading"]')))
    print('12')
    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'idDivBktDatetimeDatePickerIcon'))).click()
    print('13')
    time.sleep(3)
    elements = driver.find_elements_by_xpath("//table[@class='ui-datepicker-calendar']//td")
    print('14')
    time.sleep(3)
    dates = []
    if len(elements):
        for element in elements:
            if element.get_attribute("title") not in ('', 'CLOSED'):
                dates.append(f'{element.text}:{element.get_attribute("title")}')
    screen = driver.get_screenshot_as_png()
    driver.quit()
    return dates, screen
