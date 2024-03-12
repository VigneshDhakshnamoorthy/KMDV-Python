import allure
import pytest
from core.kmdv.util.selenium_util import SeleniumUtil
from pages.HomePage import HomePage
from selenium.webdriver.common.by import By

@allure.suite("Sauce Labs Tests")
class TestSauceLab:
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_sauce_lab_1(self, selenium: SeleniumUtil) -> None:
        homePage = HomePage(selenium)
        homePage.open_app().login_to_app("standard_user", "secret_sauce")
        homePage.add_product(
            "Sauce Labs Onesie"
            if "chrome" in selenium.get_browser_name().lower()
            else "Sauce Labs Backpack"
        )
        selenium.get_element_screenshot(homePage.CART_ITEM_COUNT, "element screen shot")
        assert homePage.get_cart_count() == (
            1 if "chrome" in selenium.get_browser_name().lower() else 2
        ), "Assertion error message for test_sauce_lab_1"

    @pytest.mark.regression
    @pytest.mark.dev
    def test_sauce_lab_2(self, selenium: SeleniumUtil) -> None:
        homePage = HomePage(selenium)
        homePage.open_app().login_to_app("standard_user", "secret_sauce")
        homePage.add_product(
            "Sauce Labs Backpack"
            if "chrome" in selenium.get_browser_name().lower()
            else "Sauce Labs Onesie"
        )
        selenium.get_element_screenshot(homePage.CART_ITEM_COUNT, "element screen shot")
        assert homePage.get_cart_count() == (
            2 if "chrome" in selenium.get_browser_name().lower() else 1
        ), "Assertion error message for test_sauce_lab_2"
        
    @pytest.mark.skip
    def test_sauce_lab_3(self, selenium: SeleniumUtil) -> None:
        homePage = HomePage(selenium)
        homePage.open_app().login_to_app("standard_user", "secret_sauce")
        
    @pytest.mark.dev
    def test_sauce_lab_4(self, selenium: SeleniumUtil) -> None:
        homePage = HomePage(selenium)
        homePage.open_app().login_to_app("standard_user", "secret_sauce")
        homePage.add_product(
            "Sauce Labs Backpack"
            if "chrome" in selenium.get_browser_name().lower()
            else "Sauce Labs Onesie"
        )
        selenium.get_element_screenshot(homePage.CART_ITEM_COUNT, "element screen shot")
        assert homePage.get_cart_count() == (
            1 if "chrome" in selenium.get_browser_name().lower() else 2
        ), "Assertion error message for test_sauce_lab_1"


    @pytest.mark.multi_instance
    def test_sauce_lab_5(self, selenium: SeleniumUtil) -> None:
        selenium.open("http://www.google.com")
        selenium.create_driver_instance("bing","firefox")
        selenium.switch_driver_instance("bing")
        selenium.open("https://www.bing.com/")
        selenium.switch_driver_instance()
        selenium.type_enter((By.XPATH, "//*[@name='q']"),"Vignesh Dhakshnamoorthy")
        selenium.switch_driver_instance("bing")
        selenium.type_enter((By.XPATH, "//*[@id='sb_form_q']"),"Vignesh Dhakshnamoorthy")
        selenium.sleep_for_seconds(5)
        selenium.switch_driver_instance().back()
        selenium.switch_driver_instance("bing").back()

        selenium.sleep_for_seconds(2)