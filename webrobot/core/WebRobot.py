from selenium import webdriver

class WebRobot:

    @staticmethod
    def driver(headless=True):
        options = webdriver.FirefoxOptions()
        if headless: options.add_argument("--headless")  # run as headless will not render a browser window
        return webdriver.Firefox(options=options)  #  may need to sudo apt install firefox-geckodriver or brew install geckodriver
