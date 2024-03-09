from enum import Enum
from selenium import webdriver
from selenium.webdriver import Chrome, Edge, Firefox

class BrowserName(Enum):
    CHROME:str = 'Chrome'
    FIREFOX:str = 'Firefox'
    EDGE:str = 'Edge'
    
    @staticmethod
    def keys():
        return list(BrowserName.__members__.keys())

    @staticmethod
    def values():
        return list(BrowserName.__members__.values())
    
    @classmethod
    def get_value(cls, key:str):
        return cls[key.upper()].value if key.upper() in cls.__members__ else None

class BrowserUtil:
    
    def __init__(self, browserName:str) -> None:
        self.browserName = browserName.lower().strip()

    def get_driver(self) -> Chrome | Edge | Firefox:
        match self.browserName:
            case "chrome":
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("--disable-extensions")
                return webdriver.Chrome(options=chrome_options)            
            case "edge":
                edge_options = webdriver.EdgeOptions()
                edge_options.add_argument("--disable-extensions")
                edge_options.add_argument("--enable-chrome-browser-cloud-management")
                return webdriver.Edge(options=edge_options)
            case "firefox":
                firefox_options = webdriver.FirefoxOptions()
                return webdriver.Firefox(options=firefox_options)
            case "chromeheadless":
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("--disable-extensions")
                chrome_options.add_argument("--headless")
                return webdriver.Chrome(options=chrome_options)
            case "edgeheadless":
                edge_options = webdriver.EdgeOptions()
                edge_options.use_chromium = True
                edge_options.add_argument("--disable-extensions")
                edge_options.add_argument("--headless")
                return webdriver.Edge(options=edge_options)
            case "firefoxheadless":
                firefox_options = webdriver.FirefoxOptions()
                firefox_options.headless = True
                return webdriver.Firefox(options=firefox_options)
            case _:
                raise ValueError(f"Unsupported browser: {self.browserName}")
