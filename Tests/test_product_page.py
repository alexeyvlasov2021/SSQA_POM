import time

from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By

from Config.config import TestData
from Pages.LandingPage import LandingPage
from Tests.test_base import TestBase
import pytest
import allure


class TestProductPage(TestBase):
    def test_product_page_url(self):
        landing_page = LandingPage(self.driver)
        text = TestData.SEARCH_PRODUCT_TEXT_QUERY
        expected_url = TestData.PRODUCT_PAGE_URL

        # after search query is applied, product page is opened
        product_page = landing_page.search_product(text_query=text)

        assert product_page.is_page_url_displayed(expected_url), (f'wrong page url: \'{self.driver.current_url}\'.'
                                                                  f'expected page url: \'{expected_url}\'')

    def test_total_price_cart(self):
        # method run is skipped
        # pytest.skip("method to be implemented")

        landing_page = LandingPage(self.driver)
        text = TestData.SEARCH_PRODUCT_TEXT_QUERY

        # after search query is applied, product page is opened
        product_page = landing_page.search_product(text_query=text)
        amount = TestData.INCREASE_COUNT_TO_VALUE
#         to be implemented:
#           -clicking Add button
#           -validation of total amount
        product_page.add_to_cart(amount=amount)
        item_price_text = product_page.get_element_text(product_page.ITEM_PRICE_LOC).strip('$')
        item_price_value = float(item_price_text)
        total_price_text = product_page.get_element_text(product_page.PRICE_TOTAL_TEXT_LOC).strip('$')
        total_price_value = float(total_price_text)

        assert amount * item_price_value == total_price_value , (f'wrong total price value: \'{amount * item_price_value}\'. '
                                                                 f'expected total price value: \'{total_price_value}\'')

        # same assert but with integration of screens to allure report
        # if amount * item_price_value == total_price_value:
        #     assert True
        # else:
        #     # total_price_element = self.driver.find_element(product_page.PRICE_TOTAL_TEXT_LOC[0], product_page.PRICE_TOTAL_TEXT_LOC[1])
        #     # total_price_element = self.driver.find_element(By.CSS_SELECTOR, 'a > span.woocommerce-Price-amount.amount')

        # option 1: attached screen of the element
        #     # allure.attach(total_price_element.screenshot_as_png,
        #     #               name='test_total_price_cart_screenshot',
        #     #               attachment_type=AttachmentType.PNG)
        #
        # option 2: attached screen of the entire page
        #     allure.attach(self.driver.get_screenshot_as_png(),
        #                   name='test_total_price_cart_screenshot',
        #                   attachment_type=AttachmentType.PNG)
        #     assert False, (f'wrong total price value: \'{amount * item_price_value}\'. '
        #                                                          f'expected total price value: \'{total_price_value}\'')


    def test_add_multiple_items_to_cart(self):
        landing_page = LandingPage(self.driver)
        product_page = landing_page.open_product(index=3)

        product_page.click_add_cart()
        product_page.is_element_displayed(product_page.SUCCESS_MSG_LOC)
        product_page.go_to_home_page()
        landing_page.open_product(index=2)
        product_page.click_add_cart()