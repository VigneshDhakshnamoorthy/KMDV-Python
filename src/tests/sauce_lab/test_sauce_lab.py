import allure
import pytest
from core.kmdv.util.selenium_util import SeleniumUtil
from pages.HomePage import HomePage

@allure.suite("Sauce Labs Tests")
class TestSauceLab:
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_sauce_lab_1(self, selenium: SeleniumUtil) -> None:
        homePage = HomePage(selenium)
        homePage.open_app().login_to_app("standard_user", "secret_sauce")
        homePage.add_product(
            "Sauce Labs Onesie"
            if selenium.get_browser_name().lower() == "chrome"
            else "Sauce Labs Backpack"
        )
        selenium.get_element_screenshot(homePage.CART_ITEM_COUNT, "element screen shot")
        assert homePage.get_cart_count() == (
            1 if selenium.get_browser_name().lower() == "chrome" else 2
        ), "Assertion error message for test_sauce_lab_1"

    @pytest.mark.regression
    @pytest.mark.dev
    def test_sauce_lab_2(self, selenium: SeleniumUtil) -> None:
        homePage = HomePage(selenium)
        homePage.open_app().login_to_app("standard_user", "secret_sauce")
        homePage.add_product(
            "Sauce Labs Backpack"
            if selenium.get_browser_name().lower() == "chrome"
            else "Sauce Labs Onesie"
        )
        selenium.get_element_screenshot(homePage.CART_ITEM_COUNT, "element screen shot")
        assert homePage.get_cart_count() == (
            1 if selenium.get_browser_name().lower() == "chrome" else 2
        ), "Assertion error message for test_sauce_lab_2"
