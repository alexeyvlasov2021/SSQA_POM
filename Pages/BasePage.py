from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver : WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_page_url_displayed(self, url):
        try:
            self.wait.until(expected_conditions.url_to_be(url))
            return True
        except TimeoutException:
            return False

    def do_click(self, by_locator : tuple[str, str]):
        self.wait.until(expected_conditions.element_to_be_clickable(by_locator)).click()

    def do_send_keys(self, by_locator : tuple[str, str], text):
        element = self.wait.until(expected_conditions.element_to_be_clickable(by_locator))
        element.send_keys(text)
        element.send_keys(Keys.ENTER)

    def is_page_title_displayed(self, title):
        try:
            self.wait.until(expected_conditions.title_is(title))
            return True
        except TimeoutException:
            return False

    def get_element_text(self, by_locator : tuple[str, str]):
        element = self.wait.until(expected_conditions.visibility_of_element_located(by_locator))
        return element.text

    def is_text_displayed(self, text, by_locator : tuple[str, str]):
        try:
            self.wait.until(expected_conditions.text_to_be_present_in_element(by_locator, text))
            return True
        except TimeoutException:
            return False
        # self.wait.until(expected_conditions.text_to_be_present_in_element(by_locator, text))

    def is_element_displayed(self, by_locator : tuple[str, str]):
        try:
            self.wait.until(expected_conditions.visibility_of_element_located(by_locator))
            return True
        except TimeoutException:
            return False
