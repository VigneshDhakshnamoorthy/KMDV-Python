import pandas as pd
from time import sleep
import pytest
import allure

from core.kmdv.util.selenium_util import SeleniumUtil


@pytest.mark.smoke
def test_sample1(selenium: SeleniumUtil):
    selenium.open("https://www.google.com")
    selenium.log("test_sample1")
    selenium.sleepSeconds(2)
    assert True


@pytest.mark.smoke
def test_sample2(selenium: SeleniumUtil):
    selenium.open("https://www.google.com")
    selenium.log("test_sample2")
    selenium.sleepSeconds(2)
    assert False


@pytest.mark.skip
def test_sample3(selenium: SeleniumUtil):
    selenium.open("https://www.google.com")
    selenium.log("test_sample3")
    selenium.sleepSeconds(2)
    assert True


@pytest.mark.skip
def test_sample4(selenium: SeleniumUtil):
    selenium.open("https://www.google.com")
    selenium.log("test_sample4")
    selenium.sleepSeconds(2)
    assert True


@pytest.mark.skip
def test_sample5(selenium: SeleniumUtil):
    selenium.open("https://www.google.com")
    selenium.log("test_sample5")
    selenium.sleepSeconds(2)
    assert True

"""

pytest
pytest -s = print statement
pytest -s -k test_sample1 = specific testcase
pytest -s -m smoke = run only specific tagged testcases

"""
