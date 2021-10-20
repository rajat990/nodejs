import time

import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from logUtil import logger
from selenium.webdriver.chrome.service import Service

import config

BROWSER_WAIT = 10
s=Service("C:\driver\chromedriver.exe")
@pytest.fixture(scope="session")
def login_chatbot():
    user_data = config.read_ini()
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    options.add_argument("--disable-extensions");
    options.add_argument("test-type");
    options.add_argument("--ignore-certificate-errors");
    options.add_argument("no-sandbox");
    web_driver = webdriver.Chrome(service=s, options=options)
    web_driver.implicitly_wait(BROWSER_WAIT)
    web_driver.delete_all_cookies()
    web_driver.maximize_window()
    web_driver.get(user_data.get('user_info', 'URL'))
    delay = 60  # seconds
    try:
        WebDriverWait(web_driver, delay).until(
            EC.presence_of_element_located((By.XPATH,
                    "//*[@class='slds-dropdown-trigger slds-dropdown-trigger_click slds-avatar_circle profile_menu']"))
        )
    except TimeoutException:
        logger("Loading took too much time!")
    time.sleep(3)
    web_driver.find_element_by_xpath("//*[@class='slds-dropdown-trigger slds-dropdown-trigger_click slds-avatar_circle profile_menu']").click()
    web_driver.implicitly_wait(BROWSER_WAIT)
    try:
        web_driver.find_element_by_xpath("//a[contains(text(), 'Sign In')]").click()
        web_driver.implicitly_wait(BROWSER_WAIT)
        username = web_driver.find_element_by_id("username")
        username.clear()
        username.send_keys(user_data.get('user_info','USER'))

        password = web_driver.find_element_by_id("password")
        password.clear()
        password.send_keys(user_data.get('user_info','PASSWORD'))
        web_driver.find_element_by_id("signIn").click()
        web_driver.implicitly_wait(BROWSER_WAIT)
        if web_driver.find_element_by_class_name("slds-modal__container").is_displayed():
            web_driver.find_element_by_xpath("//*[@class='slds-p-around_xx-small slds-max-small-size_1-of-1']").click()
    except Exception as e:
        logger.info("User already logged in")

    yield web_driver
    web_driver.quit()
    logger.info("Webdriver connection closed..")

@pytest.fixture()
def click_chatbot(login_chatbot):
    window_before = login_chatbot.window_handles[0]
    login_chatbot.implicitly_wait(BROWSER_WAIT)
    login_chatbot.find_element_by_xpath("//*[@class='hpe-floating-chat-icon-container']").click()

    window_after = login_chatbot.window_handles[1]
    login_chatbot.switch_to.window(window_after)
    login_chatbot.implicitly_wait(5)
    return login_chatbot

def pytest_addoption(parser):
    parser.addoption("--user_data", action="store", default="default file")


@pytest.fixture()
def user_data(pytestconfig):
    return pytestconfig.getoption("user_data")
