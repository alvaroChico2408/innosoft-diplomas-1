from selenium.webdriver.common.by import By

from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import initialize_driver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
        self.driver.find_element(By.ID, "email").send_keys("user1@example.com")
        self.driver.find_element(By.ID, "password").send_keys("password")
        self.driver.find_element(By.ID, "submit").click()
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".welcome-box h2.display-4.text-primary"))
            )
            
            welcome_message = self.driver.find_element(By.CSS_SELECTOR, ".welcome-box h2.display-4.text-primary")
            assert "Bienvenido a Diplomas INNOSOFT" in welcome_message.text

        except Exception as e:
            raise e