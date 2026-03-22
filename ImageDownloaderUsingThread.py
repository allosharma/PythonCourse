import time
import threading
import requests
import uuid

class ImageDownloader(threading.Thread):
    def __init__(self, url, filename):
        threading.Thread.__init__(self)
        self.url = url
        self.filename = filename

    def run(self):
        print(f'Starting download of {self.url} in thread {threading.current_thread().name}')
        response = requests.get(self.url)
        with open(self.filename, 'wb') as f:
            f.write(response.content)
        print(f'Finished downloading {self.url} in thread {threading.current_thread().name}')

if __name__ == "__main__":
    start_time = time.time()
    urls = [
        'https://images.pexels.com/photos/414612/pexels-photo-414612.jpeg',
        'https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg',
        'https://images.pexels.com/photos/1108098/pexels-photo-1108098.jpeg',
        'https://images.pexels.com/photos/414612/pexels-photo-414612.jpeg',
        'https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg',
        'https://images.pexels.com/photos/1108098/pexels-photo-1108098.jpeg',
        'https://images.pexels.com/photos/414612/pexels-photo-414612.jpeg',
        'https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg',
        'https://images.pexels.com/photos/1108098/pexels-photo-1108098.jpeg',
        'https://images.pexels.com/photos/414612/pexels-photo-414612.jpeg',
        'https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg',
        'https://images.pexels.com/photos/1108098/pexels-photo-1108098.jpeg'
        'https://images.pexels.com/photos/414612/pexels-photo-414612.jpeg',
        'https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg',
        'https://images.pexels.com/photos/1108098/pexels-photo-1108098.jpeg']
    threads = []
    for i, url in enumerate(urls):
        thread = ImageDownloader(url, f'{str(uuid.uuid4())}.jpg') # This will generate a unique filename for each image using uuid
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(f"All images have been downloaded in {round(time.time() - start_time, 2)} seconds")