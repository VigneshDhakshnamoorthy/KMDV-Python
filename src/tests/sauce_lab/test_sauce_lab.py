import allure
import pytest
from pages.HomePage import HomePage


@pytest.mark.smoke
@pytest.mark.regression
def test_sauce_lab_1(selenium) -> None:
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
    )


@pytest.mark.regression
@pytest.mark.dev
def test_sauce_lab_2(selenium) -> None:
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
    )
