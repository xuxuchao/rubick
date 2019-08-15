import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from utils.log import logging, log_action


class Sensors(object):
    def __init__(self, headless=True):
        options = webdriver.ChromeOptions()
        options.add_argument('disable-infobars')
        if headless:
            options.add_argument('headless')
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)

    def login(self, username, password, project='测试项目'):
        self.driver.get("https://sensorsdata.secoo.com")
        # js = 'document.querySelector(".selector>select").removeAttribute("style")'
        # self.driver.execute_script(js)

        # project = Select(self.driver.find_element_by_css_selector(".selector>select"))
        # project.select_by_visible_text("测试项目")
        logging.info("[神策]登录({})".format(project))
        self.driver.find_element_by_id("userName").send_keys(username)
        self.driver.find_element_by_id("password").send_keys(password)
        self.driver.find_element_by_id('rememberme').click()
        self.driver.find_element_by_id("submit").click()

    def start_check(self, event, user_id):
        logging.info("[神策]点击埋点")
        self.driver.find_element_by_id("vtrack_manager_btn").click()
        logging.info("[神策]选择导入实时查看")
        self.driver.find_element_by_css_selector(".tab-item[data-method='data-stream']").click()
        logging.info("[神策]选择导入中数据")
        self.driver.find_element_by_link_text("导入中数据").click()
        self.driver.find_element_by_id("imported-users").send_keys(user_id)
        self.driver.find_element_by_id("imported-events").send_keys(event)
        logging.info("[神策]开始刷新")
        self.driver.find_element_by_xpath('//div[@id="imported-container"]//button[@data-method="resume"]').click()

    def get_data(self):
        logging.info("[神策]检测数据")
        wait = WebDriverWait(self.driver, 60)
        try:
            data = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//div[@id="imported-content-container"]'
                           '/div[@class="content-item"]'
                           '/div[@class="content-item-json"]'
                           '/div[@class="data-json"]')))
        except TimeoutException:
            return None
        else:
            return json.loads(data.text)

    def __del__(self):
        self.driver.quit()


