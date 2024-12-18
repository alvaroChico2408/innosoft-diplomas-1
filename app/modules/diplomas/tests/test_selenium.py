from selenium.webdriver.common.by import By
from core.environment.host import get_host_for_selenium_testing

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.selenium.common import initialize_driver
from app.modules.conftest import login_selenium
from selenium.webdriver.common.action_chains import ActionChains
import time
import pytest


class TestDiplomas:
    
    diploma_generator_button = ".sidebar-item:nth-child(4) .align-middle:nth-child(2)"
    diplomas_visualization_button = ".sidebar-item:nth-child(5) .align-middle:nth-child(2)"
    template_management_button = ".sidebar-item:nth-child(6) .align-middle:nth-child(2)"

    def setup_method(self, method):
        self.driver = initialize_driver()

    def teardown_method(self, method):
        self.driver.quit()

    @pytest.mark.usefixtures("populate_diplomas_with_pdfs")
    def test_ver_diploma(self):
        self.driver.maximize_window()
        login_selenium(self.driver, "user1@example.com", "password")

        # Navegar a la visualización de diplomas
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.diplomas_visualization_button))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "View"))).click()

        time.sleep(2)

    @pytest.mark.usefixtures("populate_diplomas_with_pdfs")
    def test_filtra_diplomas(self):
        self.driver.maximize_window()
        login_selenium(self.driver, "user1@example.com", "password")

        # Filtrar diplomas
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.diplomas_visualization_button))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-info:nth-child(3)"))).click()
        
        filters = [
            ".btn-light:nth-child(1)",
            ".btn-light:nth-child(2)",
            ".btn-light:nth-child(3)"
        ]
        
        # Aplicar filtros
        for filter_button in filters:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, filter_button))).click()

        # Buscar y cerrar el filtro de UVUS
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-warning"))).click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "uvusFilter"))).send_keys("alearasan")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-secondary"))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-close"))).click()

    @pytest.mark.usefixtures("populate_diplomas_with_pdfs")
    def test_borra_diploma(self):
        self.driver.maximize_window()
        login_selenium(self.driver, "user1@example.com", "password")

        # Eliminar un diploma
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.diplomas_visualization_button))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "tr:nth-child(1) form > .btn"))).click()

        # Confirmar la eliminación
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        assert alert.text == "Are you sure you want to delete this diploma?"
        alert.dismiss()

    @pytest.mark.usefixtures("populate_diplomas_with_pdfs")
    def test_borra_todos_diplomas(self):
        self.driver.maximize_window()
        login_selenium(self.driver, "user1@example.com", "password")

        # Eliminar todos los diplomas
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.diplomas_visualization_button))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-dark:nth-child(1)"))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-danger:nth-child(3)"))).click()

        # Confirmar la eliminación
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        assert alert.text == "Are you sure you want to delete the selected diplomas?"
        alert.dismiss()

    def test_ver_plantilla(self):
        self.driver.maximize_window()
        login_selenium(self.driver, "user1@example.com", "password")

        # Navegar a la gestión de plantillas
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.template_management_button))).click()

        # Ver plantilla
        view_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Ver")))
        
        # Desplazar a la plantilla y hacer clic
        self.driver.execute_script("arguments[0].scrollIntoView(true);", view_button)
        self.driver.execute_script("arguments[0].click();", view_button)

        time.sleep(2)

    def test_borra_plantilla(self):
        self.driver.maximize_window()
        login_selenium(self.driver, "user1@example.com", "password")

        # Hacer clic en el botón de "Gestión de Plantillas"
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.template_management_button))).click()

        # Esperar a que el botón de "Eliminar" sea clickeable
        delete_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-danger")))

        # Desplazar al botón y hacer clic usando ActionChains
        actions = ActionChains(self.driver)
        actions.move_to_element(delete_button).click().perform()

        # Confirmar la eliminación
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        assert alert.text == "¿Estás seguro de eliminar esta plantilla?"

        # Descartar el alert
        alert.dismiss()

        time.sleep(2)

    def test_bienvenido_a_diplomas(self):
        # Abre la página que contiene el <h2>
        self.driver.get(get_host_for_selenium_testing())

        # Espera a que el elemento <h2> esté presente
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h2.display-4.text-primary'))
        )

        # Encuentra el elemento <h2> con la clase correcta
        h2_element = self.driver.find_element(By.CSS_SELECTOR, 'h2.display-4.text-primary')

        # Verifica que el texto del elemento sea "Bienvenido a Diplomas"
        assert "BIENVENIDO A DIPLOMAS" in h2_element.text, f"Se esperaba 'BIENVENIDO A DIPLOMAS', pero se encontró: {h2_element.text}"
        
        time.sleep(2)