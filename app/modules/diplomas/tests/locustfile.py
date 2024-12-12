from locust import HttpUser, TaskSet, task, between
import json
from core.locust.common import get_csrf_token, fake
from core.environment.host import get_host_for_locust_testing


class DiplomaBehavior(TaskSet):
    wait_time = between(5, 15)  # Tiempo de espera entre las tareas de cada usuario
    host = get_host_for_locust_testing()  # Host para las pruebas

    def on_start(self):
        """ Se ejecuta al inicio de cada usuario para simular el login """
        self.login()

    def login(self):
        """ Simula un login exitoso """
        response = self.client.get("/login")
        csrf_token = get_csrf_token(response)

        login_data = {
            "email": 'user1@example.com',
            "password": 'password',
            "csrf_token": csrf_token
        }

        self.client.post("/login", data=login_data)

    @task(1)
    def generate_diplomas(self):
        """ Simula la creación de diplomas sin subir un archivo Excel real """
        response = self.client.get("/diplomas")  # Abrir el formulario para generar diplomas
        csrf_token = get_csrf_token(response)

        # Enviar los datos necesarios para generar los diplomas, sin un archivo Excel real
        # Suponiendo que se necesita seleccionar una plantilla (ID 1) y pasar un CSRF token
        form_data = {
            "template": "1",  # ID de la plantilla seleccionada (ajústalo según sea necesario)
            "csrf_token": csrf_token
        }

        response = self.client.post("/diplomas", data=form_data)
        if response.status_code == 302:  # Redirección después de un envío exitoso
            print("Diplomas generados con éxito")
        else:
            print(f"Error al generar diplomas: {response.status_code}")

    @task(2)
    def diplomas_visualization(self):
        """ Simula la visualización de diplomas generados """
        response = self.client.get("/diplomas-visualization")
        if response.status_code == 200:
            print("Diplomas visualizados con éxito")
        else:
            print(f"Error al visualizar diplomas: {response.status_code}")

    @task(3)
    def view_diploma(self):
        """ Simula la visualización de un diploma específico """
        diploma_id = 1  # Asume que existe un diploma con ID 1
        response = self.client.get(f"/view_diploma/{diploma_id}")
        if response.status_code == 200:
            print(f"Diploma {diploma_id} visualizado con éxito")
        else:
            print(f"Error al visualizar diploma {diploma_id}: {response.status_code}")

    @task(1)
    def delete_diploma(self):
        """ Simula la eliminación de un diploma """
        diploma_id = 1  # Asume que existe un diploma con ID 1
        response = self.client.post(f"/delete_diploma/{diploma_id}", data={"_method": "DELETE"})
        if response.status_code == 302:  # Redirección después de la eliminación
            print(f"Diploma {diploma_id} eliminado con éxito")
        else:
            print(f"Error al eliminar diploma {diploma_id}: {response.status_code}")

    @task(1)
    def manage_templates(self):
        """ Simula la gestión de plantillas (subir, visualizar, eliminar) """
        # Subir plantilla
        response = self.client.get("/manage-templates")
        csrf_token = get_csrf_token(response)

        with open("docs/plantillas/Plantilla diploma.pdf", "rb") as file:
            files = {
                "pdf_file": file,
                "custom_text": "Texto personalizado de prueba",
                "csrf_token": csrf_token
            }

            response = self.client.post("/manage-templates", files=files)
            if response.status_code == 302:
                print("Plantilla subida con éxito")
            else:
                print(f"Error al subir plantilla: {response.status_code}")

        # Visualizar plantilla
        template_id = 1  # Asume que existe una plantilla con ID 1
        response = self.client.get(f"/view_template/{template_id}")
        if response.status_code == 200:
            print(f"Plantilla {template_id} visualizada con éxito")
        else:
            print(f"Error al visualizar plantilla {template_id}: {response.status_code}")

        # Eliminar plantilla
        response = self.client.post(f"/delete_template/{template_id}", data={"_method": "DELETE"})
        if response.status_code == 302:
            print(f"Plantilla {template_id} eliminada con éxito")
        else:
            print(f"Error al eliminar plantilla {template_id}: {response.status_code}")

class DiplomasUser(HttpUser):
    tasks = [DiplomaBehavior]
    min_wait = 5000
    max_wait = 9000
    host = get_host_for_locust_testing()