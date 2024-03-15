from datetime import datetime
import json
import os
import re
import shutil
import subprocess
import psutil
from lxml import etree, html

from core.kmdv.config.browser_config import BrowserConfig


class TestRunner:
    @staticmethod
    def kill_webdriver_processes():
        webdriver_names = ["chromedriver.exe", "msedgedriver.exe", "geckodriver.exe"]
        for process in psutil.process_iter(attrs=["pid", "name"]):
            for name in webdriver_names:
                if name in process.info["name"]:
                    psutil.Process(process.info["pid"]).terminate()

    @staticmethod
    def remove_cache_directories(directory, folder_name):
        for root, dirs, files in os.walk(directory):
            if folder_name in dirs:
                cache_dir = os.path.join(root, folder_name)
                try:
                    for item in os.listdir(cache_dir):
                        item_path = os.path.join(cache_dir, item)
                        if os.path.isfile(item_path):
                            os.unlink(item_path)
                        else:
                            for sub_item in os.listdir(item_path):
                                sub_item_path = os.path.join(item_path, sub_item)
                                os.unlink(sub_item_path)
                            os.rmdir(item_path)
                    os.rmdir(cache_dir)
                except Exception as e:
                    print(f"Error removing {folder_name} directory: {e}")

    @staticmethod
    def json_report(
        file_name,
        completed_time,
        passed_count,
        failed_count,
        skipped_count,
        test_case_list,
    ):
        date_complete = completed_time.split(" - ")[0]
        time_complete = completed_time.split(" - ")[1]

        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                data: dict = json.load(file)
                data[date_complete] = (
                    {} if date_complete not in data else data[date_complete]
                )
        else:
            data = {date_complete: {}}

        data[date_complete][time_complete] = {
            "Passed": passed_count,
            "Failed": failed_count,
            "Skipped": skipped_count,
            "Testcases": test_case_list,
        }

        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def splitString(string_value: str, start: str, end: str = None):
        if end is None:
            return string_value.split(start)[0]
        try:
            start_index = string_value.index(start) + len(start)
            end_index = string_value.index(end)
            return string_value[start_index:end_index]
        except ValueError:
            return string_value

    @staticmethod
    def add_numbers_to_duplicates(word_list):
        word_count = {}
        result = []

        for word in word_list:
            if word in word_count:
                word_count[word] += 1
                new_word = f"{word}.{word_count[word]}"
                result.append(new_word)
            else:
                word_count[word] = 0
                result.append(word)

        return result
    @staticmethod
    def run_session():
        file_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = file_dir.split("core")[0]
        allureResult = "allure-result"
        allureReport = "allure-report"
        pytestReportFolder = "pytest-report"
        pytest_html_report = "pytest.html"
        pytest_json_report = "pytest.json"
        pytest_xml_report = "pytest.xml"
        pytestHistory = "history.json"
        allure_result_path = os.path.join(project_dir, allureResult)
        allure_report_path = os.path.join(project_dir, allureReport)
        pytest_cache_folder_path = os.path.join(project_dir, ".pytest_cache")
        pytest_report_folder_path = os.path.join(project_dir, pytestReportFolder)
        pytest_html_report_path = os.path.join(
            pytest_report_folder_path, pytest_html_report
        )
        pytest_json_report_path = os.path.join(
            pytest_report_folder_path, pytest_json_report
        )
        pytest_xml_report_path = os.path.join(
            pytest_report_folder_path, pytest_xml_report
        )
        pytest_history_path = os.path.join(pytest_report_folder_path, pytestHistory)
        allure_history_source = os.path.join(project_dir, allureReport, "history")
        allure_history_target = os.path.join(project_dir, allure_result_path, "history")
        parallel_count = BrowserConfig.getParallelCount()
        parallel_count_command = (
            ""
            if parallel_count == ""
            else "" if int(parallel_count) < 2 else f"-n {parallel_count}"
        )
        allureEnable = BrowserConfig.isAllureEnable()
        tag = BrowserConfig.getTag()
        tag_command = "" if tag == "" else f"-k {tag}"
        PrintCMD = "no" if BrowserConfig.isPrintCMD() else "sys"
        commands = [
            # (
            #     f"pytest -s --alluredir={allureResult} --html={pytest_html_report_path} --self-contained-html --json={pytest_json_report_path} --junitxml={pytest_xml_report_path} {parallel_count_command} {tag_command} --capture={PrintCMD} --tb=line"
            # ),
            # f"allure generate {allureResult} --clean",
            # f"allure open",
        ]

        for folder in [
            allure_result_path,
            pytest_cache_folder_path,
        ]:
            if os.path.exists(folder):
                shutil.rmtree(folder)
                print(f"{os.path.basename(folder)} Deleted")

        for command in commands:
            if "generate" in command:
                if os.path.exists(allure_history_source) and os.path.exists(
                    allure_result_path
                ):
                    shutil.copytree(allure_history_source, allure_history_target)
                    shutil.rmtree(allure_report_path)
            if "open" in command:
                TestRunner.kill_webdriver_processes()
                TestRunner.remove_cache_directories(project_dir, "__pycache__")
                if not allureEnable:
                    break
            try:
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error running command: {command}")
            except Exception as e:
                print(f"An error occurred while running command: {command}")

        if os.path.exists(pytest_json_report_path):
            with open(pytest_json_report_path, "r") as file:
                json_report: dict = json.load(file)
            completed_time = datetime.strptime(
                (
                    str(json_report["report"]["created_at"])
                    .split(".")[0]
                    .replace(" ", " - ")
                ),
                "%Y-%m-%d - %H:%M:%S",
            ).strftime("%d-%b-%Y - %H:%M:%S")
            failed_count = (
                json_report["report"]["summary"]["failed"]
                if "failed" in json_report["report"]["summary"]
                else 0
            )
            passed_count = (
                json_report["report"]["summary"]["passed"]
                if "passed" in json_report["report"]["summary"]
                else 0
            )
            skipped_count = (
                json_report["report"]["summary"]["skipped"]
                if "skipped" in json_report["report"]["summary"]
                else 0
            )
            test_case_list_source = json_report["report"]["tests"]
            test_case_list_target = {}
            for test_case in test_case_list_source:
                test_case_outcome: str = test_case["outcome"]
                log_list = ["skipped"]
                if not test_case_outcome == "skipped":
                    log_list.clear()
                    call_log = test_case["call"]["stdout"].split("\n")[:-1]
                    teardown_log = test_case["teardown"]["stdout"].split("\n")[:-1]
                    log_list.extend(call_log)
                    log_list.extend(teardown_log)
   
                test_case_name: str = test_case["name"]
                test_case_name_list: list[str] = test_case_name.split("::",1)
                test_source_list = re.split(r'[\\\/]', test_case_name_list[0])
                folder_name = "/".join(test_source_list[:-1])
                file_name = test_source_list[-1]
                reason =  [] if not test_case_outcome == "failed" else re.split(r'[\n\t]', test_case["call"]["longrepr"])
                reason = [element.strip() for element in reason if element.strip() != ""]
                test_case_list_target[
                    f"{test_case_name_list[-1].replace('::','.').split('[')[0]}"
                ] = {"Folder":folder_name,"File":file_name,"Status": test_case_outcome.title(), "Log": log_list, "Reason" : reason}
                # print(f"{test_case_outcome} - {test_case_name_list[-2]}.{test_case_name_list[-1].split('[')[0]} - {TestRunner.splitString(test_case_name,'[',']')}")
            TestRunner.json_report(
                pytest_history_path,
                completed_time,
                passed_count,
                failed_count,
                skipped_count,
                {k: test_case_list_target[k] for k in sorted(test_case_list_target)},
            )

            print(
                f"\033[96mTest Execution Summary : {completed_time}\033[0m\n\033[92mPassed - {passed_count}\033[0m\n\033[91mFailed - {failed_count}\033[0m\n\033[93mSkipped - {skipped_count}\033[0m"
            )
