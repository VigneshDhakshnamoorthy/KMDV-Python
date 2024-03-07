import sys
import pandas as pd
import pytest
from core.kmdv.config.browser_config import BrowserConfig
from core.kmdv.base.test_results import TestResults
from core.kmdv.util.selenium_util import SeleniumUtil

test_results = {}

sys.stdout = sys.stderr


def pytest_runtest_makereport(item, call) -> None:
    if not hasattr(item, "_result_printed"):
        if call.when == "setup":
            outcome = call.excinfo
            if outcome is not None:
                result = "skipped"
                TestResults.add_result(item.name, result)
            return
        if call.when == "call":
            outcome = call.excinfo
            if outcome is None:
                result = "passed"
            elif outcome.typename == "Skipped":
                result = "skipped"
            else:
                result = "failed"
            TestResults.add_result(item.name, result)
        item._result_printed = True


def getBrowserList() -> list[str]:
    if BrowserConfig.isMultiBrowser() and not BrowserConfig.isExcelData():
        return BrowserConfig.getMultiBrowserList()
    else:
        return BrowserConfig.getDefaultBrowser()


def get_browser_name_from_excel(method_name:str) -> str:
    if "[" in method_name:
        method_name = method_name.split("[")[0]

    df = pd.read_excel("resource/data/Book1.xlsx")
    browser_name = df[df["TestCaseName"].str.contains(method_name, case=False)][
        "Browser"
    ].values[0]
    return browser_name


@pytest.fixture(params=getBrowserList(), autouse=True)
def selenium(request: pytest.FixtureRequest) -> "SeleniumUtil":  # type: ignore
    method_name = request.node.name
    try:
        if BrowserConfig.isExcelData():
            browser_name: str = get_browser_name_from_excel(method_name)
        else:
            browser_name: str = request.param
    except:
        browser_name: str = request.param
    sel = SeleniumUtil(browser_name)
    sel.log(f"Opening : {browser_name.title()} Browser")
    yield sel
    if TestResults.get_result(method_name) == "failed":
        sel.get_screenshot("screen shot | failure")
    sel.quit()
    sel.log(f"Closing : {browser_name.title()} Browser")
    sel.sleep_for_seconds(2)