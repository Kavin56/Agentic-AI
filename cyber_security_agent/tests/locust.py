#locust -f locust.py --host=https://taupe-tanuki-66c44a.netlify.app

from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    # Wait between 1 and 5 seconds between tasks
    wait_time = between(1, 5)

    # Define a task to simulate visiting the homepage
    @task
    def load_homepage(self):
        self.client.get("/")

    # Define additional tasks for other pages or API endpoints
    @task
    def load_contact_page(self):
        self.client.get("/contact")
