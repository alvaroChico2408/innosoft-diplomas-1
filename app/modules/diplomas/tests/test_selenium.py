from selenium.webdriver.common.by import By
from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import initialize_driver
import time


class TestTest1():
    def setup_method(self, method):
        self.driver = initialize_driver()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_ver_diploma(self):
        self.driver.get(get_host_for_selenium_testing())
        host = get_host_for_selenium_testing()
        self.driver.maximize_window()
        self.driver.get(f'{host}/login')
        self.driver.find_element(By.ID, "email").send_keys("userCliente@gmail.com")
        self.driver.find_element(By.ID, "password").send_keys("12345678!Aa")
        self.driver.find_element(By.ID, "submit").click()
        time.sleep(1)
        diploma_generator_button = ".sidebar-item:nth-child(4) .align-middle:nth-child(2)"
        diplomas_visualization_button = ".sidebar-item:nth-child(5) .align-middle:nth-child(2)"
        template_management_button = ".sidebar-item:nth-child(6) .align-middle:nth-child(2)"
        self.driver.find_element(By.CSS_SELECTOR, diplomas_visualization_button).click()
        time.sleep(2)
        self.driver.find_element(By.LINK_TEXT, "View").click()
        time.sleep(5)
        self.driver.close()

    def test_filtra_diplomas(self):
        self.driver.get(get_host_for_selenium_testing())
        host = get_host_for_selenium_testing()
        self.driver.maximize_window()
        self.driver.get(f'{host}/login')
        self.driver.find_element(By.ID, "email").send_keys("userCliente@gmail.com")
        self.driver.find_element(By.ID, "password").send_keys("12345678!Aa")
        self.driver.find_element(By.ID, "submit").click()
        time.sleep(1)
        diploma_generator_button = ".sidebar-item:nth-child(4) .align-middle:nth-child(2)"
        diplomas_visualization_button = ".sidebar-item:nth-child(5) .align-middle:nth-child(2)"
        template_management_button = ".sidebar-item:nth-child(6) .align-middle:nth-child(2)"
        self.driver.find_element(By.CSS_SELECTOR, diplomas_visualization_button).click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".btn-info:nth-child(3)").click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".btn-light:nth-child(1)").click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".btn-light:nth-child(2)").click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".btn-light:nth-child(3)").click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".btn-warning").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "uvusFilter").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "uvusFilter").send_keys("alearasan")
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".btn-secondary").click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".btn-close").click()
        time.sleep(1)
        self.driver.close()


    def test_borra_diploma(self):
        self.driver.get(get_host_for_selenium_testing())
        host = get_host_for_selenium_testing()
        self.driver.maximize_window()
        self.driver.get(f'{host}/login')
        self.driver.find_element(By.ID, "email").send_keys("userCliente@gmail.com")
        self.driver.find_element(By.ID, "password").send_keys("12345678!Aa")
        self.driver.find_element(By.ID, "submit").click()
        time.sleep(1)
        diploma_generator_button = ".sidebar-item:nth-child(4) .align-middle:nth-child(2)"
        diplomas_visualization_button = ".sidebar-item:nth-child(5) .align-middle:nth-child(2)"
        template_management_button = ".sidebar-item:nth-child(6) .align-middle:nth-child(2)"
        self.driver.find_element(By.CSS_SELECTOR, diplomas_visualization_button).click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) form > .btn").click()
        time.sleep(1)
        assert self.driver.switch_to.alert.text == "Are you sure you want to delete this diploma?"
        time.sleep(1)
        self.driver.switch_to.alert.accept()
        time.sleep(2)
        self.driver.close()

    def test_borra_todos_diplomas(self):
        self.driver.get(get_host_for_selenium_testing())
        host = get_host_for_selenium_testing()
        self.driver.maximize_window()
        self.driver.get(f'{host}/login')
        self.driver.find_element(By.ID, "email").send_keys("userCliente@gmail.com")
        self.driver.find_element(By.ID, "password").send_keys("12345678!Aa")
        self.driver.find_element(By.ID, "submit").click()
        time.sleep(1)
        diploma_generator_button = ".sidebar-item:nth-child(4) .align-middle:nth-child(2)"
        diplomas_visualization_button = ".sidebar-item:nth-child(5) .align-middle:nth-child(2)"
        template_management_button = ".sidebar-item:nth-child(6) .align-middle:nth-child(2)"
        self.driver.find_element(By.CSS_SELECTOR, diplomas_visualization_button).click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".sidebar-item:nth-child(5) .align-middle:nth-child(2)").click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".btn-dark:nth-child(1)").click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".btn-danger:nth-child(3)").click()
        time.sleep(1)
        self.driver.close()