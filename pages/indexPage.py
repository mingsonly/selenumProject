from pages.basepage import BasePage
from selenium.webdriver.common.by import By


class IndexPage(BasePage):
    title_loc = (By.XPATH, '//*[@id="app"]/div[1]/div[1]/div/div[1]/a/h1')

    def get_title(self):
        title = self.get_element(self.title_loc).text
        return title
