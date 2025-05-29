import time

import pytest
from allure_commons.types import AttachmentType
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from Config.config import TestData
from Pages.LandingPage import LandingPage
from Tests.test_base import TestBase
import allure

# define severity level for test class
# @allure.severity(allure.severity_level.NORMAL)
class TestLandingPage(TestBase):
    @allure.severity(allure.severity_level.MINOR)
    def test_nav_items_count(self):
        landing_page = LandingPage(self.driver)
        items_count = landing_page.get_nav_items_count()
        # assert items_count == TestData.NAV_ITEMS_COUNT, 'wrong nav items count'
        if items_count == TestData.NAV_ITEMS_COUNT:
            assert True
        else:
            # attach screenshot of define name, type PNG to the allure report
            # allure.attach(self.driver.get_screenshot_as_png(), name='test_nav_items_screenshot',
            #               attachment_type= AttachmentType.PNG)

            # collect and attach screenshot of web element, not the hole page
            nav_menu = self.driver.find_element(By.CSS_SELECTOR, "ul.nav-menu")
            allure.attach(nav_menu.screenshot_as_png, name='test_nav_items_screenshot',
                          attachment_type= AttachmentType.PNG)
            assert False, 'wrong count of navigation elements'

    def test_to_be_skipped(self):
        # write your comment or reason here:
        pytest.skip('this test will be implemented later')

    def test_page_title(self):
        expected_title = TestData.LANDING_PAGE_TITLE
        landing_page = LandingPage(self.driver)
        assert landing_page.is_page_title_displayed(expected_title), (f"expected page title: '{expected_title}'. actual"
                                                              f"page title is '{self.driver.title}'")
    def test_adding_to_cart(self):
        landing_page = LandingPage(self.driver)
        expected_text = TestData.CART_COUNT_TEXT_VALUE
        item_locator = landing_page.CART_COUNT_TXT
        landing_page.add_to_cart(1)
        landing_page.add_to_cart(3)
        assert landing_page.is_text_displayed(expected_text, item_locator), \
            (f'unexpected cart items count: \'{landing_page.get_element_text(item_locator)}\'.'
             f'expected count: \'{expected_text}\'')

    def test_total_cart_price(self):
        landing_page = LandingPage(self.driver)
        expected_text = TestData.CART_COUNT_TEXT_VALUE
        item_locator = landing_page.CART_COUNT_TXT

        landing_page.add_to_cart(1)
        landing_page.add_to_cart(3)

        # this method call adds wait. it is critical for waiting till last cart is added
        landing_page.is_text_displayed(expected_text, item_locator)

        total_item_locator = landing_page.CART_ITEMS_TOTAL_PRICE
        total_expected_text = TestData.CART_ITEMS_TOTAL_PRICE_VALUE
        total_actual_text = landing_page.get_element_text(total_item_locator)

        assert total_expected_text == total_actual_text, (f'unexpected cart price total: \'{total_actual_text}\','
                                                          f'expected total: \'{total_expected_text}\'')


    # def test_remove_from_cart(self):
    #     pytest.skip("test drops on firefox. needs debugging")
    #     landing_page = LandingPage(self.driver)
    #     expected_text = TestData.CART_COUNT_TEXT_VALUE
    #     item_locator = landing_page.CART_COUNT_TXT
    #
    #     landing_page.add_to_cart(1)
    #     landing_page.add_to_cart(3)
    #
    #     # this method call adds wait. it is critical for waiting till last cart is added
    #     landing_page.is_text_displayed(expected_text, item_locator)
    #
    #     # hover the cart count area with mouse to see pop-up
    #     ActionChains(self.driver) \
    #         .move_to_element(self.driver.find_element(item_locator[0], item_locator[1])) \
    #         .move_by_offset(xoffset=50, yoffset=0) \
    #         .perform()
    #
    #     landing_page.remove_from_cart()
    #
    #     new_expected_text = TestData.CART_COUNT_TEXT_DEFAULT_VALUE
    #
    #     assert landing_page.is_text_displayed(text=new_expected_text, by_locator=item_locator)

    def test_front_message(self):
        landing_page = LandingPage(self.driver)
        message = TestData.LANDING_PAGE_FRONT_MESSAGE
        message_locator = landing_page.FRONT_MESSAGE_LOC

        assert landing_page.is_text_displayed(text=message, by_locator=message_locator), \
            (f"wrong landing page front text message: \'{landing_page.get_element_text(message_locator)} \'."
             f"expected message {message}")


    def absence_of_element(self):
        try:
            return WebDriverWait(self.driver, 0.5).until(expected_conditions.invisibility_of_element(
                (By.XPATH, '//*[@id="site-header-cart"]/li[2]/div/div/p[2]/a[2]')))
        except TimeoutException:
            return False

    def test_remove_cart_items(self):
        landing_page = LandingPage(self.driver)
        landing_page.add_to_cart(1)
        landing_page.add_to_cart(3)

        is_count_displayed = landing_page.is_text_displayed(text=TestData.CART_COUNT_TEXT_VALUE,
                                                            by_locator=landing_page.CART_COUNT_TXT)

        actual_text = self.driver.find_element(landing_page.CART_COUNT_TXT[0],
                                               landing_page.CART_COUNT_TXT[1]).text

        assert is_count_displayed, f'wrong count is displayed: {actual_text}. expected text: {TestData.CART_COUNT_TEXT_VALUE}'
        WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(landing_page.CART_COUNT_TXT))

        count_element = self.driver.find_element(By.CSS_SELECTOR, 'a.cart-contents')

        ActionChains(driver=self.driver, duration=1000) \
            .move_to_element(to_element=count_element) \
            .move_by_offset(xoffset=50, yoffset=0) \
            .perform()


        btns_list = WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, 'a[aria-label="Remove this item"]')))

        while True:
            btns_list[0].click()
            time.sleep(2)
            btns_list = self.driver.find_elements(By.CSS_SELECTOR, 'a[aria-label="Remove this item"]')
            if not self.absence_of_element():
                continue
            else:
                break