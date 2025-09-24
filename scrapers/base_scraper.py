# scrapers/base_scraper.py
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time

class BaseScraper:
    def __init__(self, headless=True, driver_path=None):
        opts = Options()
        if headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        # add user-agent
        opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140 Safari/537.36")
        self.driver = webdriver.Chrome(options=opts)  # dev: ensure chromedriver in PATH

    def close(self):
        try:
            self.driver.quit()
        except:
            pass

    def wait(self, seconds=1.0):
        time.sleep(seconds)

    def search(self, **kwargs):
        raise NotImplementedError("override in subclass")