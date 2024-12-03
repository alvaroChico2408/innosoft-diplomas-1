from selenium.webdriver.common.by import By

from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import initialize_driver
import time

class TestLogin():
    def setup_method(self, method):
        self.driver = initialize_driver()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_login(self):
        self.driver.get(get_host_for_selenium_testing())
        host = get_host_for_selenium_testing()
        self.driver.get(f'{host}/login')
        self.driver.find_element(By.ID, "email").send_keys("userCliente@gmail.com")
        self.driver.find_element(By.ID, "password").send_keys("123456789!Aa")
        self.driver.find_element(By.ID, "submit").click()