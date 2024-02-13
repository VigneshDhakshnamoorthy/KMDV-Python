import pandas as pd
from time import sleep
import pytest

@pytest.mark.smoke
def test_sample9(driver):
    driver.get("https://www.google.com")
    sleep(2)
    assert True

@pytest.mark.smoke
def test_sample2(driver):
    driver.get("https://www.google.com")
    sleep(2)
    assert False

@pytest.mark.skip
def test_sample3(driver):
    driver.get("https://www.google.com")
    sleep(2)
    assert True
    
    
"""

pytest
pytest -s = print statement
pytest -s -k test_sample1 = specific testcase
pytest -s -m smoke = run only specific tagged testcases

"""