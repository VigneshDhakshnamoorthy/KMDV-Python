import configparser

class BrowserConfig:
    iniFilePath: str = "resource/config/browserConfig.ini"
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
        multiBrowserList: list[str] = BrowserConfig.config.get("BrowserConfig", "MultiBrowserList").split(",")
        if not BrowserConfig.isHeadless():
            return [browser for browser in multiBrowserList]
        else:
            return [f"{browser}headless" for browser in multiBrowserList]

    @staticmethod
    def getDefaultBrowser() -> list[str]:
        defaultBrowser: str = BrowserConfig.config.get("BrowserConfig", "DefaultBrowser")
        if not BrowserConfig.isHeadless():
            return [defaultBrowser]
        else:
            return [f"{defaultBrowser}headless"]

    @staticmethod
    def getParallelCount() -> str:
        return BrowserConfig.config.get("BrowserConfig", "Parallel")
    
    @staticmethod
    def getTag() -> str:
        return BrowserConfig.config.get("BrowserConfig", "Tag")
    
    @staticmethod
    def getURL() -> str:
        return BrowserConfig.config.get("BrowserConfig", "URL")
    
    @staticmethod
    def isPrintCMD() -> bool:
        return BrowserConfig.config.getboolean("BrowserConfig", "PrintCMD")