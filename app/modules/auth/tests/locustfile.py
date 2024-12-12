from locust import HttpUser, TaskSet, task
from core.locust.common import get_csrf_token, fake
from core.environment.host import get_host_for_locust_testing


class LoginBehavior(TaskSet):
    def on_start(self):
        """ Se ejecuta al inicio de cada usuario virtual para asegurar que no esté autenticado. """
        self.ensure_logged_out()
        self.login()

    @task
    def ensure_logged_out(self):
        """ Asegura que el usuario esté desconectado. Si está autenticado, cierra sesión. """
        response = self.client.get("/logout")
        if response.status_code != 302:  # 302 es el código para redirección después de logout
            print(f"Logout failed or no active session: {response.status_code}")
        else:
            print("Successfully logged out.")

    @task
    def login(self):
        """ Realiza el login con un correo y contraseña predefinidos. """
        response = self.client.get("/login")
        if response.status_code != 200 or "Login" not in response.text:
            print("Already logged in or unexpected response, redirecting to logout.")
            self.ensure_logged_out()
            response = self.client.get("/login")

        csrf_token = get_csrf_token(response)

        # Datos de login estáticos (puedes hacerlo dinámico si lo prefieres)
        login_data = {
            "email": 'user1@example.com',
            "password": 'password',
            "csrf_token": csrf_token
        }

        response = self.client.post("/login", data=login_data)
        if response.status_code != 302:  # Después de un login exitoso, esperamos una redirección
            print(f"Login failed: {response.status_code}")
        else:
            print(f"Login success: {login_data['email']}")

class AuthUser(HttpUser):
    """ Clase principal que ejecuta las tareas de autenticación. """
    tasks = [LoginBehavior]
    min_wait = 5000  # Tiempo mínimo de espera entre solicitudes (5 segundos)
    max_wait = 9000  # Tiempo máximo de espera entre solicitudes (9 segundos)
    host = get_host_for_locust_testing()  # Obtiene la URL base para las pruebas

