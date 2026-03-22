from celery import shared_task
import time
import os
import requests


@shared_task
def add(x, y):
    time.sleep(2)
    return x + y

@shared_task
def download_image(url, save_path, filename):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    filename = os.path.join(save_path, filename)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    return filename
    