from typing import Callable, List, Literal, Union
import allure
import pytest
from core.kmdv.config.browser_config import BrowserConfig
from core.kmdv.config.customException import ElementNotFound
from core.kmdv.util.browser_util import BrowserName, BrowserUtil
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import Chrome, Edge, Firefox
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from allure_commons.types import AttachmentType
from time import sleep
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select


class SeleniumUtil:
    def __init__(self, browser_name: str, method_name: str) -> None:
        self.browserName = browser_name
        self.methodName = method_name
        self.waitTime = 15
        self.driver_instance = {}
        self.driver = BrowserUtil(self.browserName).get_driver()
        self.driver_instance["Default"] = [self.browserName, self.driver]

    def log(self, message) -> "SeleniumUtil":
        tc_name = f"{self.methodName} | " if BrowserConfig.isPrintCMD() else ""
        print(f"{tc_name}{message}")
        with allure.step(message):
            pass
        return self

    def sleep_for_seconds(self, waitseconds: int) -> "SeleniumUtil":
        sleep(waitseconds)
        return self

    def get_browser_name(self) -> str:
        return self.browserName

    def get_driver(self) -> Chrome | Edge | Firefox:
        return self.driver

    def create_driver_instance(
        self, name: str, browser_name: str = None
    ) -> "SeleniumUtil":
        if browser_name is None:
            self.driver_instance[name] = [
                self.browserName,
                BrowserUtil(self.browserName).get_driver(),
            ]
        else:
            is_browser_name = BrowserName.get_value(browser_name)
            if is_browser_name:
                self.driver_instance[name] = [
                    is_browser_name,
                    BrowserUtil(is_browser_name).get_driver(),
                ]
            else:
                self.driver_instance[name] = [
                    self.browserName,
                    BrowserUtil(self.browserName).get_driver(),
                ]
        return self

    def switch_driver_instance(self, name: str = None) -> "SeleniumUtil":
        if name is None:
            self.driver = self.driver_instance["Default"][1]
        else:
            self.driver = self.driver_instance[name][1]
        return self

    def get_driver_instance_name(self) -> str:
        for key, value in self.driver_instance.items():
            if value[1] == self.driver:
                return key

    def open(self, url) -> "SeleniumUtil":
        while True:
            try:
                self.driver.implicitly_wait(self.waitTime)
                self.driver.maximize_window()
                break
            except NoSuchWindowException:
                instance = self.get_driver_instance_name()
                print("Error : Browsing context has been discarded. Retrying...")
                self.driver.quit()
                self.driver = BrowserUtil(
                    self.driver_instance[instance][0]
                ).get_driver()
                self.driver_instance[instance] = [
                    self.driver_instance[instance][0],
                    self.driver,
                ]

        self.get_driver().get(url)
        if len(self.driver_instance) > 1:
            self.log(
                f"Opening : {self.driver_instance[self.get_driver_instance_name()][0].title()} / {self.get_driver_instance_name().title()} Browser Instance"
            )
        else:
            self.log(
                f"Opening : {self.driver_instance[self.get_driver_instance_name()][0].title()} Browser"
            )
        return self

    def get_title(self) -> str:
        return self.get_driver().title

    def quit(self) -> "SeleniumUtil":
        for instance in self.driver_instance:
            self.switch_driver_instance(instance)
            self.get_driver().quit()
            if len(self.driver_instance) > 1:
                self.log(
                    f"Closing : {self.driver_instance[instance][0].title()} / {instance.title()} Browser Instance"
                )
            else:
                self.log(
                    f"Closing : {self.driver_instance[instance][0].title()} Browser"
                )
        return self

    def close(self) -> "SeleniumUtil":
        self.get_driver().close()
        return self

    def back(self) -> "SeleniumUtil":
        self.get_driver().back()

    def wait_until(self, method: Callable):
        return WebDriverWait(
            driver=self.get_driver(), timeout=self.waitTime, poll_frequency=1
        ).until(method)

    def find_element(self, by: By) -> WebElement:
        try:
            return self.wait_until(lambda wd: wd.find_element(*by))
        except Exception as e:
            raise ElementNotFound(str(by))

    def get_element_text(self, by: By) -> str:
        return self.find_element(by).text

    def get_element_attribute(self, by: By, attribute: str) -> str:
        return self.find_element(by).get_attribute(attribute)

    def find_elements(self, by: By) -> list[WebElement]:
        return self.wait_until(lambda wd: wd.find_elements(*by))

    def get_text_list_from_elements(self, by: By) -> list[str]:
        elements: list[WebElement] = self.find_elements(by)
        return [element.text for element in elements]

    def click(self, by: By) -> "SeleniumUtil":
        self.find_element(by).click()
        return self

    def js_click(self, by: By) -> "SeleniumUtil":
        self.get_driver().execute_script("arguments[0].click();", self.find_element(by))
        return self

    def scroll_into_view(self, by: By) -> "SeleniumUtil":
        self.get_driver().execute_script(
            "arguments[0].scrollIntoView();", self.find_element(by)
        )
        return self

    def type(self, by: By, value: str) -> "SeleniumUtil":
        self.find_element(by).send_keys(value)
        return self

    def js_type(self, by: By, value: str) -> "SeleniumUtil":
        self.get_driver().execute_script(
            "arguments[0].value = arguments[1];", self.find_element(by), value
        )
        return self

    def type_enter(self, by: By, value: str) -> "SeleniumUtil":
        self.find_element(by).send_keys(value + Keys.ENTER)
        return self

    def type_tab(self, by: By, value: str) -> "SeleniumUtil":
        self.find_element(by).send_keys(value + Keys.TAB)
        return self

    def type_return(self, by: By, value: str) -> "SeleniumUtil":
        self.find_element(by).send_keys(value + Keys.RETURN)
        return self

    def is_enabled(self, by: By) -> bool:
        return self.find_element(by).is_enabled()

    def is_displayed(self, by: By) -> bool:
        return self.find_element(by).is_displayed()

    def is_selected(self, by: By) -> bool:
        return self.find_element(by).is_selected()

    def switch_default(self) -> "SeleniumUtil":
        self.get_driver().switch_to.default_content()
        return self

    def switch_frame(self, frame: str | int) -> "SeleniumUtil":
        self.get_driver().switch_to.frame(frame)
        return self

    def refresh(self) -> "SeleniumUtil":
        self.get_driver().refresh()
        return self

    def hover(self, by: By) -> "SeleniumUtil":
        ActionChains(self.driver).move_to_element(self.find_element(by)).perform()
        return self

    def right_click(self, by: By) -> "SeleniumUtil":
        ActionChains(self.driver).context_click(self.find_element(by)).perform()
        return self

    def current_window_handle(self) -> str:
        return self.get_driver().current_window_handle

    def window_handles(self) -> list[str]:
        return self.get_driver().window_handles

    def switch_to_child_window(self) -> "SeleniumUtil":
        parent_window: str = self.current_window_handle()
        all_windows: list[str] = self.window_handles()
        for window_handle in all_windows:
            if not window_handle == parent_window:
                self.get_driver().switch_to.window(window_handle)
                break
        return self

    def get_screenshot(self, screenshotName: str) -> "SeleniumUtil":
        screen_shot: bytes = self.get_driver().get_screenshot_as_png()
        allure.attach(
            screen_shot,
            name=screenshotName,
            attachment_type=AttachmentType.PNG,
        )
        return self

    def get_element_screenshot(self, by: By, screenshotName: str) -> "SeleniumUtil":
        allure.attach(
            self.find_element(by).screenshot_as_png,
            name=screenshotName,
            attachment_type=AttachmentType.PNG,
        )
        return self

    def clear(self, by: By) -> "SeleniumUtil":
        self.find_element(by).clear()
        return self

    def get_dropdown(self, by: By) -> Select:
        return Select(self.find_element(by))

    def select_by_visible_text(self, by: By, visible_text: str) -> "SeleniumUtil":
        self.get_dropdown(by).select_by_visible_text(visible_text)
        return self

    def select_by_index(self, by: By, index: int) -> "SeleniumUtil":
        self.get_dropdown(by).select_by_index(index)
        return self

    def select_by_value(self, by: By, value: str) -> "SeleniumUtil":
        self.get_dropdown(by).select_by_value(value)
        return self

    def get_dropdown_options(self, by: By) -> List[WebElement]:
        return self.get_dropdown(by).options

    def get_dropdown_option_values(self, by: By) -> List[str]:
        return [option.text for option in self.get_dropdown_options(by)]

    def deselect_by_visible_text(self, by: By, visible_text: str) -> "SeleniumUtil":
        self.get_dropdown(by).deselect_by_visible_text(visible_text)
        return self

    def deselect_by_index(self, by: By, index: int) -> "SeleniumUtil":
        self.get_dropdown(by).deselect_by_index(index)
        return self

    def deselect_by_value(self, by: By, value: str) -> "SeleniumUtil":
        self.get_dropdown(by).deselect_by_value(value)
        return self

    def switch_to_alert(self) -> Alert:
        return self.wait_alert_is_present()

    def alert_send_keys(self, value: str) -> "SeleniumUtil":
        self.switch_to_alert().send_keys(value)
        return self

    def alert_text(self) -> str:
        return self.switch_to_alert().text

    def alert_accept(self) -> "SeleniumUtil":
        self.switch_to_alert().accept()
        return self

    def alert_dismiss(self) -> "SeleniumUtil":
        self.switch_to_alert().dismiss()
        return self

    def wait_visibility_of_element_located(self, by: By) -> WebElement | Literal[False]:
        return self.wait_until(EC.visibility_of_element_located(by))

    def wait_invisibility_of_element_located(self, by: By) -> WebElement | bool:
        return self.wait_until(EC.invisibility_of_element_located(by))

    def wait_presence_of_element_located(self, by: By) -> WebElement:
        return self.wait_until(EC.presence_of_element_located(by))

    def wait_alert_is_present(self) -> Alert | Literal[False]:
        return self.wait_until(EC.alert_is_present())

    def wait_element_to_be_clickable(self, by: By) -> WebElement | Literal[False]:
        return self.wait_until(EC.element_to_be_clickable(by))

    def wait_frame_to_be_available_and_switch_to_it(self, value: By | str) -> bool:
        return self.wait_until(EC.frame_to_be_available_and_switch_to_it(value))

    def wait_element_to_be_selected(self, by: By) -> bool:
        return self.wait_until(EC.element_to_be_selected(self.find_element(by)))

    def wait_visibility_of_all_elements_located(
        self, by: By
    ) -> List[WebElement] | Literal[False]:
        return self.wait_until(EC.visibility_of_all_elements_located(by))

    def wait_visibility_of_any_elements_located(self, by: By) -> List[WebElement]:
        return self.wait_until(EC.visibility_of_any_elements_located(by))

    def wait_staleness_of(self, by: By) -> bool:
        return self.wait_until(EC.staleness_of(self.find_element(by)))

    def is_element_present_in_any_frame(self, by: By) -> int | None:
        iframes:list[WebElement] = self.find_elements((By.TAG_NAME, "iframe"))
        print(len(iframes))
        try:
            for frame in iframes:
                self.switch_frame(frame)
                if self.find_elements(by):
                    return i
                self.switch_default()
            return None
        except Exception as e:
            print("An error occurred:", str(e))
            return None
