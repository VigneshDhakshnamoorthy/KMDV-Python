import configparser
import os


class ConfigReader:
    def __init__(self, fileName : str) -> None:
        self.iniFilePath = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ),
            "config",
            f"{fileName}.ini",
        )
        self.config = configparser.ConfigParser()
        self.config.read(self.iniFilePath)
        
    def getConfig(self) -> configparser:
        return self.config

    def isExcelData(self) -> bool:
        return self.config.getboolean("BrowserConfig", "ExcelData")
    def isAllureEnable(self) -> bool:
        return self.config.getboolean("BrowserConfig", "AllureEnable")

    def isMultiBrowser(self) -> bool:
        return self.config.getboolean("BrowserConfig", "MultiBrowser")
    
    def isHeadless(self) -> bool:
        return self.config.getboolean("BrowserConfig", "Headless")
    
    def getMultiBrowserList(self) -> list[str]:
        self.multiBrowserList = self.config.get("BrowserConfig", "MultiBrowserList").split(",")
        if not self.isHeadless():
            return [browser.lower().strip() for browser in self.multiBrowserList]
        else:
            return [f"{browser.lower().strip()}headless" for browser in self.multiBrowserList]
    
    def getDefaultBrowser(self) -> list[str]:
        self.defaultBrowser = self.config.get("BrowserConfig", "DefaultBrowser")
        if not self.isHeadless():
            return [self.defaultBrowser.lower().strip()]
        else:
            return [f"{self.defaultBrowser.lower().strip()}headless"]
    
    def getParallelCount(self) -> str:
        return self.config.get("BrowserConfig", "Parallel")
        
    def getAppURL(self) -> str:
        return self.config.get("AppConfig", "AppURL")


    