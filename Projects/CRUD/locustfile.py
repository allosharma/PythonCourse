from locust import HttpUser, task, between
from faker import Faker
import random

# locust -f .\locustfile.py

faker = Faker('en_IN')

class WebsiteUser(HttpUser):
    @task(5)
    def get_product(self):
        self.client.get("/api/products/1", name="/api/products/[id]")
        
    @task(3)
    def submit_feedback(self):
        feedback_data = {
            "name": faker.name(),
            "email": faker.email(),
            "message": faker.text(max_nb_chars=200)
        }
        self.client.post("/api/feedback/", json=feedback_data, name="/api/feedback")
        
    @task(2)
    def get_details(self):
        product_id = random.randint(1, 200)  # Assuming you have products with IDs from 1 to 10
        self.client.get(f"/api/products/{product_id}/", name="/api/products/[id]")
        