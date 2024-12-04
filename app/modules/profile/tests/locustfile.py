from locust import HttpUser, TaskSet, task
from core.locust.common import get_csrf_token, fake
from core.environment.host import get_host_for_locust_testing


class ProfileBehavior(TaskSet):
    def on_start(self):
        self.profile()

    @task
    def profile(self):
        response = self.client.get("/profile/edit")
        if response.status_code != 200:
            print(f"Edit profile failed: {response.status_code}")


class AuthUser(HttpUser):
    tasks = [ProfileBehavior]
    min_wait = 5000
    max_wait = 9000
    host = get_host_for_locust_testing()