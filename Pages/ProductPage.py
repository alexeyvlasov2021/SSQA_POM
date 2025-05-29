from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions

from Config.config import TestData
from Pages.BasePage import BasePage


class ProductPage(BasePage):
    def __init__(self, driver : WebDriver):
        super().__init__(driver)

    ITEM_COUNT_LOC = (By.XPATH, '//input[@type="number"][contains(@id, "quantity_")]')
    ADD_TO_CART_BTN_LOC = (By.CSS_SELECTOR, 'button[name="add-to-cart"]')
    ITEM_PRICE_LOC = (By.CSS_SELECTOR, 'p.price span.woocommerce-Price-amount.amount')
    PRICE_TOTAL_TEXT_LOC = (By.CSS_SELECTOR, 'a > span.woocommerce-Price-amount.amount')
    HOME_LNK_LOC = (By.XPATH, '//ul[@class="nav-menu"]/li/a[text()="Home"]')
    SUCCESS_MSG_LOC = (By.CSS_SELECTOR, 'div.woocommerce-message')
    TOTAL_ITEMS_COUNT_LOC = (By.XPATH, '//*[@id="site-header-cart"]/li[1]/a/span[2]')

    def increase_count(self, amount):
        input_number = self.wait.until(expected_conditions.element_to_be_clickable(self.ITEM_COUNT_LOC))
        for _ in range(1, amount):
            input_number.send_keys(Keys.ARROW_UP)

    def add_to_cart(self, amount):
        self.increase_count(amount)
        self.do_click(self.ADD_TO_CART_BTN_LOC)
        self.wait.until(expected_conditions.text_to_be_present_in_element(self.TOTAL_ITEMS_COUNT_LOC, f'{amount}'))

    def click_add_cart(self):
        self.do_click(self.ADD_TO_CART_BTN_LOC)

    def go_to_home_page(self):
        self.do_click(self.HOME_LNK_LOC)