import configparser
import os

class BrowserConfig:
    iniFilePath = "resource/config/browserConfig.ini"
    config = configparser.ConfigParser()
    config.read(iniFilePath)

    @staticmethod
    def getConfig() -> configparser:
        return BrowserConfig.config
    
    @staticmethod
    def isExcelData() -> bool:
        return BrowserConfig.config.getboolean("BrowserConfig", "ExcelData")
    
    @staticmethod
    def isAllureEnable() -> bool:
        return BrowserConfig.config.getboolean("BrowserConfig", "AllureEnable")

    @staticmethod
    def isMultiBrowser() -> bool:
        return BrowserConfig.config.getboolean("BrowserConfig", "MultiBrowser")

    @staticmethod
    def isHeadless() -> bool:
        return BrowserConfig.config.getboolean("BrowserConfig", "Headless")
    
    @staticmethod
    def getMultiBrowserList() -> list[str]:
        multiBrowserList = BrowserConfig.config.get("BrowserConfig", "MultiBrowserList").split(",")
        if not BrowserConfig.isHeadless():
            return [browser.lower().strip() for browser in multiBrowserList]
        else:
            return [f"{browser.lower().strip()}headless" for browser in multiBrowserList]

    @staticmethod
    def getDefaultBrowser() -> list[str]:
        defaultBrowser = BrowserConfig.config.get("BrowserConfig", "DefaultBrowser")
        if not BrowserConfig.isHeadless():
            return [defaultBrowser.lower().strip()]
        else:
            return [f"{defaultBrowser.lower().strip()}headless"]

    @staticmethod
    def getParallelCount() -> str:
        return BrowserConfig.config.get("BrowserConfig", "Parallel")
    
    @staticmethod
    def getURL() -> str:
        return BrowserConfig.config.get("BrowserConfig", "URL")
