import sys
import threading
from time import sleep
import pandas as pd
import pytest
from core.kmdv.util.browser_util import BrowserUtil
from pytest import StashKey, CollectReport
from typing import Dict
from core.kmdv.base.test_results import TestResults
from core.kmdv.util.selenium_util import SeleniumUtil

phase_report_key = StashKey[Dict[str, CollectReport]]()
test_results ={}

sys.stdout = sys.stderr


def pytest_runtest_makereport(item, call):
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


@pytest.fixture
def selenium(request) -> SeleniumUtil: # type: ignore
    method_name = request.node.name
    try:
        browser_name = get_browser_name_from_excel(method_name)
    except:
        browser_name ="chrome"
    sel = SeleniumUtil(browser_name)
    sel.log(f"Opening : {sel.getBrowserName()} Browser")
    yield sel
    if TestResults.get_result(method_name) == "failed":
        sel.getScreenshot("Screenshot")
    sel.quit()
    sel.log(f"Closing : {sel.getBrowserName()} Browser")
    sleep(2)



def get_browser_name_from_excel(method_name):
    df = pd.read_excel('resource/data/Book1.xlsx')
    browser_name = df.loc[df["TestCaseName"] == method_name, 'Input'].values[0]
    print(f"\nTestCase Name: {method_name}, Browser Name: {browser_name}")
    return browser_name


def pytest_sessionfinish(session, exitstatus):
    TestResults.print_results()


