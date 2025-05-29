import time

from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions

from Config.config import TestData
from Pages.BasePage import BasePage
from Pages.ProductPage import ProductPage


class LandingPage(BasePage):
    def __init__(self, driver : WebDriver):
        super().__init__(driver)
        # prevents from some drops of Explicit Wait on Chrome
        time.sleep(0.5)
        driver.get(TestData.BASE_URL)
        # Delete all cookies
        driver.delete_all_cookies()
        driver.maximize_window()

    NAV_ITEMS = (By.CSS_SELECTOR, "ul.nav-menu li")
    ADD_TO_CART_BTNS = (By.XPATH, '//a[contains(@class, "add_to_cart_button")][contains(text(), "Add to cart")]')
    CART_COUNT_TXT = (By.CSS_SELECTOR, 'a.cart-contents span.count')
    CART_ITEMS_TOTAL_PRICE = (By.CSS_SELECTOR, 'span.woocommerce-Price-amount.amount')
    CART_REMOVE_BTNS = (By.CSS_SELECTOR, 'a[aria-label="Remove this item"]')
    FRONT_MESSAGE_LOC = (By.CSS_SELECTOR, 'div.wpfront-message.wpfront-div')
    SEARCH_PRODUCT_LOC = (By.CSS_SELECTOR, 'input#woocommerce-product-search-field-0')
    PRODUCT_ICONS_LIST_LOC = (By.CSS_SELECTOR, 'ul.products.columns-4 > li > a > img')
    PRODUCT_ICONS_CONTAINER_LOC = (By.CSS_SELECTOR, 'ul.products.columns-4')


    def get_nav_items_count(self):
        items_list = self.wait.until(expected_conditions.visibility_of_any_elements_located(self.NAV_ITEMS))
        items_count = len(items_list)
        return items_count

    def add_to_cart(self, index):
        self.wait.until(expected_conditions.visibility_of_any_elements_located(self.ADD_TO_CART_BTNS))
        btns = self.driver.find_elements(self.ADD_TO_CART_BTNS[0], self.ADD_TO_CART_BTNS[1])
        btns[index].click()

    def remove_from_cart(self):
        # btns_list = self.wait.until(expected_conditions.visibility_of_all_elements_located(self.CART_REMOVE_BTNS))
        self.wait.until(expected_conditions.visibility_of_all_elements_located(self.CART_REMOVE_BTNS))
        btns_list = self.driver.find_elements(self.CART_REMOVE_BTNS[0], self.CART_REMOVE_BTNS[1])

        while len(btns_list) > 0:
            btns_list[0].click()
            time.sleep(2)
            btns_list = self.driver.find_elements(self.CART_REMOVE_BTNS[0], self.CART_REMOVE_BTNS[1])

        # time.sleep(1)
        #
        # l = len(btns_list)
        #
        # while l > 0:
        #     btns_list[0].click()
        #
        #     while l > len(self.driver.find_elements(self.CART_REMOVE_BTNS[0], self.CART_REMOVE_BTNS[1])):
        #         time.sleep(2)
        #
        #     btns_list = self.driver.find_elements(self.CART_REMOVE_BTNS[0], self.CART_REMOVE_BTNS[1])
        #     l = len(btns_list)

    def search_product(self, text_query):
        locator = self.SEARCH_PRODUCT_LOC
        self.do_send_keys(by_locator=locator, text=text_query)
        product_page = ProductPage(self.driver)
        return product_page

    def open_product(self, index):
        # self.wait.until(expected_conditions.visibility_of_any_elements_located(self.PRODUCT_ICONS_LIST_LOC))


        # is_loaded = self.is_page_title_displayed(TestData.LANDING_PAGE_TITLE)
        # self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="main"]/ul/li[16]/a[1]/img')))
        # icons_list = self.driver.find_elements(self.PRODUCT_ICONS_LIST_LOC[0], self.PRODUCT_ICONS_LIST_LOC[1])
        icons_list = self.wait.until(expected_conditions.visibility_of_all_elements_located((By.CSS_SELECTOR, 'ul.products.columns-4 > li > a > img')))

        if icons_list:
            icon = icons_list[index]
            # self.wait.until(expected_conditions.element_to_be_clickable(icon))
            icon.click()
            return ProductPage(self.driver)
        else:
            return None


