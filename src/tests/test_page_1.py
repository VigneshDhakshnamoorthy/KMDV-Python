import pytest


@pytest.mark.smoke
def test_sample1(selenium) -> None:
    selenium.open("https://www.google.com").log("test_sample1").sleepSeconds(2)
    assert True


@pytest.mark.smoke
def test_sample2(selenium) -> None:
    selenium.open("https://www.google.com").log("test_sample2").sleepSeconds(2)
    assert False


@pytest.mark.skip
def test_sample3(selenium) -> None:
    selenium.open("https://www.google.com").log("test_sample3").sleepSeconds(2)
    assert True


@pytest.mark.skip
def test_sample4(selenium) -> None:
    selenium.open("https://www.google.com").log("test_sample4").sleepSeconds(2)
    assert True


@pytest.mark.skip
def test_sample5(selenium) -> None:
    selenium.open("https://www.google.com").log("test_sample5").sleepSeconds(2)
    assert True


"""

pytest
pytest -s = print statement
pytest -s -k test_sample1 = specific testcase
pytest -s -m smoke = run only specific tagged testcases

"""
