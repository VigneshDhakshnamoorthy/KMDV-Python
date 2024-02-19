import os
import shutil
import subprocess
import psutil

from core.kmdv.config.browser_config import BrowserConfig

project_dir = os.path.dirname(os.path.abspath(__file__))
allureResult = "allure-result"
allureReport = "allure-report"
allure_result_path = os.path.join(project_dir, allureResult)
allure_report_path = os.path.join(project_dir, allureReport)
allure_history_source = os.path.join(project_dir, allureReport, "history")
allure_history_target = os.path.join(project_dir, allure_result_path, "history")

parallel_count = BrowserConfig.getParallelCount()
allureEnable:bool = BrowserConfig.isAllureEnable()

commands = [
    f"pytest -s -v --alluredir={allureResult} -n {parallel_count}",
    f"allure generate {allureResult} --clean",
    f"allure open",
]

def kill_webdriver_processes() -> None:
    webdriver_names = ["chromedriver.exe", "msedgedriver.exe", "geckodriver.exe"]
    for process in psutil.process_iter(attrs=["pid", "name"]):
        for name in webdriver_names:
            if name in process.info["name"]:
                psutil.Process(process.info["pid"]).terminate()
                print(name)
                
def pytest_session():    
    if os.path.exists(allure_result_path):
        shutil.rmtree(allure_result_path)
        print("Allure Result Folder Deleted")

    for command in commands:
        if "generate" in command:
            if os.path.exists(allure_history_source) and os.path.exists(allure_result_path):
                shutil.copytree(allure_history_source, allure_history_target)
                shutil.rmtree(allure_report_path)
        if "open" in command:
            kill_webdriver_processes()
            if not allureEnable:
                break
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {command}")
        except Exception as e:
            print(f"An error occurred while running command: {command}")
            

pytest_session()


