from locust import HttpUser, TaskSet, task, between
from core.locust.common import get_csrf_token, fake
from core.environment.host import get_host_for_locust_testing

class ProfileBehavior(TaskSet):
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
    def edit_profile(self):
        """ Simula la edición del perfil de usuario """
        response = self.client.get("/profile/edit")  # Obtener el formulario de edición de perfil
        csrf_token = get_csrf_token(response)

        form_data = {
            "name": "Test",  # Cambiar el nombre
            "surname": "User",  # Cambiar el apellido
            "email": "new_email@example.com",  # Cambiar el email
            "csrf_token": csrf_token
        }

        response = self.client.post("/profile/edit", data=form_data)
        if response.status_code == 302:  # Redirección después de una actualización exitosa
            print("Perfil actualizado con éxito")
        else:
            print(f"Error al actualizar el perfil: {response.status_code}")

    @task(2)
    def change_password(self):
        """ Simula el cambio de contraseña de usuario """
        response = self.client.get("/profile/change_password")  # Obtener el formulario para cambiar la contraseña
        csrf_token = get_csrf_token(response)

        form_data = {
            "password": "new_secure_password",  # Nueva contraseña
            "confirm_password": "new_secure_password",  # Confirmar la nueva contraseña
            "csrf_token": csrf_token
        }

        response = self.client.post("/profile/change_password", data=form_data)
        if response.status_code == 302:  # Redirección después de una actualización exitosa
            print("Contraseña cambiada con éxito")
        else:
            print(f"Error al cambiar la contraseña: {response.status_code}")

class ProfileUser(HttpUser):
    tasks = [ProfileBehavior]
    min_wait = 5000  # Tiempo mínimo entre tareas
    max_wait = 9000  # Tiempo máximo entre tareas
    host = get_host_for_locust_testing()
