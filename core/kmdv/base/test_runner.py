import os
import shutil
import subprocess
import time
import psutil
from lxml import etree

from core.kmdv.config.browser_config import BrowserConfig


class TestRunner:
    @staticmethod
    def kill_webdriver_processes():
        webdriver_names = ["chromedriver.exe", "msedgedriver.exe", "geckodriver.exe"]
        for process in psutil.process_iter(attrs=["pid", "name"]):
            for name in webdriver_names:
                if name in process.info["name"]:
                    psutil.Process(process.info["pid"]).terminate()
                    print(name)

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
    def run_session():
        file_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = file_dir.split("core")[0]
        allureResult = "allure-result"
        allureReport = "allure-report"
        pytestReportFolder = "pytest-report"
        pytestReport = "pytest.html"
        allure_result_path = os.path.join(project_dir, allureResult)
        allure_report_path = os.path.join(project_dir, allureReport)
        pytest_report_folder_path = os.path.join(project_dir, pytestReportFolder)
        pytest_report_path = os.path.join(pytest_report_folder_path, pytestReport)
        allure_history_source = os.path.join(project_dir, allureReport, "history")
        allure_history_target = os.path.join(project_dir, allure_result_path, "history")
        parallel_count = BrowserConfig.getParallelCount()
        allureEnable = BrowserConfig.isAllureEnable()
        tag = BrowserConfig.getTag()
        commands = [
            (
                f"pytest -s --alluredir={allureResult} --html={pytest_report_path} -n {parallel_count}"
                if tag == ""
                else f"pytest -s --alluredir={allureResult} --html={pytest_report_path} -n {parallel_count} -k {tag}"
            ),
            f"allure generate {allureResult} --clean",
            f"allure open",
        ]

        if os.path.exists(allure_result_path):
            shutil.rmtree(allure_result_path)
            print("Allure Result Folder Deleted")
        
        if os.path.exists(pytest_report_folder_path):
            shutil.rmtree(pytest_report_folder_path)
            print("Pytest Report Folder Deleted")

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
        
        if os.path.exists(pytest_report_path):
            with open(pytest_report_path, "r") as f:
                html_content = f.read()
            tree = etree.HTML(html_content)
            failed_count = str(tree.xpath("//span[@class='failed']/text()")[0]).split(" ")[0]
            passed_count = str(tree.xpath("//span[@class='passed']/text()")[0]).split(" ")[0]
            skipped_count = str(tree.xpath("//span[@class='skipped']/text()")[0]).split(" ")[0]
            print(f"Passed - {passed_count} ; Failed - {failed_count} ; Skipped - {skipped_count}")




            


