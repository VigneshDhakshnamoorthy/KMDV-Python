from dataclasses import Field, dataclass
from selenium.webdriver.common.by import By
from core.kmdv.config.browser_config import BrowserConfig

from core.kmdv.util.selenium_util import SeleniumUtil


@dataclass
class LoginPage:

    def __init__(self, selenium: SeleniumUtil) -> None:
        self.selenium: SeleniumUtil = selenium

    USER_NAME_INPUT: By = (By.ID, "user-name")
    PASSWORD_INPUT: By = (By.ID, "password")
    LOGIN_BUTTON: By = (By.ID, "login-button")

    def open_app(self) -> "LoginPage":
        self.selenium.open(BrowserConfig.getURL())
        return self

    def login_to_app(self, USER_NAME: str, PASSWORD: str) -> "LoginPage":
        self.selenium.type(self.USER_NAME_INPUT, USER_NAME).type(
            self.PASSWORD_INPUT, PASSWORD
        ).click(self.LOGIN_BUTTON).sleep_for_seconds(2)
        return self
