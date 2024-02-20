import allure
from core.kmdv.config.customException import ElementNotFound
from core.kmdv.util.browser_util import BrowserUtil
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import Chrome, Edge, Firefox
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from allure_commons.types import AttachmentType
from time import sleep


class SeleniumUtil:
    def __init__(self, browserName) -> None:
        self.browserName = browserName
        self.waitTime = 10
        self.driver = BrowserUtil(self.browserName).get_driver()
        self.driver.implicitly_wait(self.waitTime)
        self.driver.maximize_window()
        self.actionChains = ActionChains(self.driver)

    def log(self, message) -> "SeleniumUtil":
        print(message)
        with allure.step(message):
            pass
        return self

    def sleepSeconds(self, waitseconds: int) -> "SeleniumUtil":
        sleep(waitseconds)
        return self

    def getBrowserName(self) -> str:
        return self.browserName

    def getDriver(self) -> Chrome | Edge | Firefox:
        return self.driver

    def open(self, url) -> "SeleniumUtil":
        self.driver.get(url)
        return self

    def title(self) -> str:
        return self.driver.title

    def quit(self) -> "SeleniumUtil":
        self.driver.quit()
        return self

    def findElement(self, by: By) -> WebElement:
        try:
            return WebDriverWait(self.driver, self.waitTime).until(
                lambda wd: wd.find_element(*by)
            )
        except Exception as e:
            raise ElementNotFound(str(by))

    def getText(self, by: By) -> str:
        return self.findElement(by).text

    def findElements(self, by: By) -> list[WebElement]:
        return WebDriverWait(self.driver, self.waitTime).until(
            lambda wd: wd.find_elements(*by)
        )

    def getTextElements(self, by: By) -> list[str]:
        elements: list[WebElement] = self.findElements(by)
        return [element.text for element in elements]

    def click(self, by: By) -> "SeleniumUtil":
        self.findElement(by).click()
        return self

    def jsClick(self, by: By) -> "SeleniumUtil":
        self.driver.execute_script("arguments[0].click();", self.findElement(by))
        return self

    def scrollIntoView(self, by: By) -> "SeleniumUtil":
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", self.findElement(by)
        )
        return self

    def type(self, by: By, value: str) -> "SeleniumUtil":
        self.findElement(by).send_keys(value)
        return self


    def jsType(self, by: By, value: str) -> "SeleniumUtil":
        self.driver.execute_script(
            "arguments[0].value = arguments[1];", self.findElement(by), value
        )
        return self


    def typeEnter(self, by: By, value: str) -> "SeleniumUtil":
        self.findElement(by).send_keys(value + Keys.ENTER)
        return self


    def typeTab(self, by: By, value: str) -> "SeleniumUtil":
        self.findElement(by).send_keys(value + Keys.TAB)
        return self

    def typeReturn(self, by: By, value: str) -> "SeleniumUtil":
        self.findElement(by).send_keys(value + Keys.RETURN)
        return self

    def switchFrame(self, frame: str | int) -> "SeleniumUtil":
        self.switchDefault()
        self.driver.switch_to.frame(frame)
        return self

    def switchDefault(self) -> "SeleniumUtil":
        self.driver.switch_to.default_content()
        return self

    def refresh(self) -> "SeleniumUtil":
        self.driver.refresh()
        return self

    def hover(self, by: By) -> "SeleniumUtil":
        self.actionChains.move_to_element(self.findElement(by)).perform()
        return self

    def rightClick(self, by: By) -> "SeleniumUtil":
        self.actionChains.context_click(self.findElement(by)).perform()
        return self

    def switchtoChildWindow(self) -> "SeleniumUtil":
        parent_window: str = self.driver.current_window_handle
        all_windows: list[str] = self.driver.window_handles
        for window_handle in all_windows:
            if not window_handle == parent_window:
                self.driver.switch_to.window(window_handle)
                break
        return self

    def getScreenshot(self, screenshotName: str) -> "SeleniumUtil":
        allure.attach(
            self.getDriver().get_screenshot_as_png(),
            name=screenshotName,
            attachment_type=AttachmentType.PNG,
        )
        return self

    def alertAccept(self) -> str:
        alert = self.getDriver().switch_to.alert
        alertText = alert.text
        alert.accept()
        return alertText
