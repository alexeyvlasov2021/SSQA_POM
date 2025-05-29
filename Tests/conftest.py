import pytest
from selenium import webdriver
from selenium.webdriver.ie.webdriver import WebDriver
import time

@pytest.fixture(params=['chrome'], scope='class')
def init_driver(request):
    web_driver : WebDriver

    if request.param == 'chrome':
        web_driver = webdriver.Chrome()
    elif request.param == 'firefox':
        web_driver = webdriver.Firefox()
    elif request.param == 'safari':
        web_driver = webdriver.Safari()
    else:
        raise Exception('Wrong driver parameter in init_driver')
    request.cls.driver = web_driver
    yield
    # time.sleep(4)
    web_driver.close()
    # does not help with problem of opening Landing Page
    # web_driver.quit()