from selenium.webdriver.ie.webdriver import WebDriver
import pytest

@pytest.mark.usefixtures('init_driver')
class TestBase:
    driver : WebDriver
