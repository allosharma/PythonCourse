from locust import HttpUser, task, between, TaskSet
from random import randint
import json

class UserBehavior(TaskSet):
    @task
    def like_post(self):
        post_id = randint(1, 5)
        self.client.get(
            f'/like/{post_id}/',        # match your urls.py exactly
            data=json.dumps({}),
            headers={'Content-Type': 'application/json'}
        )

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1,2)
    host = 'http://localhost:8000'