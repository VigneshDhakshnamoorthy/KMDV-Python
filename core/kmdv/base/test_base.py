import sys
import threading
import pandas as pd
import pytest
from core.kmdv.util.browser_util import BrowserUtil
from pytest import StashKey, CollectReport
from typing import Dict

phase_report_key = StashKey[Dict[str, CollectReport]]()
test_results ={}

sys.stdout = sys.stderr


def pytest_runtest_makereport(item, call):
    if not hasattr(item, "_result_printed"):
        if call.when == "setup":
            outcome = call.excinfo
            if outcome is not None:
                result = "skipped"
                test_results[item.name] = result
            return
        if call.when == "call":
            outcome = call.excinfo
            if outcome is None:
                result = "passed"
            elif outcome.typename == "Skipped":
                result = "skipped"
            else:
                result = "failed"
            test_results[item.name] = result
        item._result_printed = True


@pytest.fixture
def driver(request):
    method_name = request.node.name
    try:
        browser_name = get_browser_name_from_excel(method_name)
    except:
        browser_name ="chrome"
    driver = BrowserUtil(browser_name).get_driver()
    driver.maximize_window()
    yield driver
    driver.quit()



def get_browser_name_from_excel(method_name):
    df = pd.read_excel('resource/data/Book1.xlsx')
    browser_name = df.loc[df["TestCaseName"] == method_name, 'Input'].values[0]
    print(f"\nTestCase Name: {method_name}, Browser Name: {browser_name}")
    return browser_name


def pytest_sessionfinish(session, exitstatus):
    print("\nTest results:")
    for test_name, result in test_results.items():
        print(f"{test_name} - Status: {result}")


