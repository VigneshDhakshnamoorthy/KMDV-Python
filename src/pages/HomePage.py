from dataclasses import Field, dataclass
from selenium.webdriver.common.by import By
from core.kmdv.config.browser_config import BrowserConfig

from core.kmdv.util.selenium_util import SeleniumUtil
from pages.LoginPage import LoginPage


@dataclass
class HomePage(LoginPage):
    selenium: SeleniumUtil

    def __init__(self, selenium: SeleniumUtil) -> None:
        self.selenium = selenium

    CART_ITEM: By = (By.XPATH, "//a[@class='shopping_cart_link']")
    CART_ITEM_COUNT: By = (By.XPATH, "//span[@class='shopping_cart_badge']")
    PRODUCT_ADD_CART: By = (
        By.XPATH,
        "//button[@class='btn btn_primary btn_small btn_inventory']",
    )
    BACK_TO_PRODUCTS: By = (
        By.XPATH,
        "//button[@class='btn btn_secondary back btn_large inventory_details_back_button']",
    )

    def add_product(self, Product_name: str) -> "HomePage":
        self.selenium.js_click((By.LINK_TEXT, Product_name)).sleep_for_seconds(1).log(
            "Product : " + Product_name + " Clicked"
        ).sleep_for_seconds(1).click(self.PRODUCT_ADD_CART).log(
            "Product : " + Product_name + " Added to Cart"
        ).sleep_for_seconds(
            1
        ).click(
            self.BACK_TO_PRODUCTS
        ).sleep_for_seconds(
            1
        )
        return self

    def get_cart_count(self) -> "HomePage":
        return int(self.selenium.get_element_text(self.CART_ITEM_COUNT))
