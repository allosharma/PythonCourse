import requests
import uuid
from bs4 import BeautifulSoup
from home.models import News
import random
from home.task import download_image


def scrape_imdb_news():
    url = 'https://www.imdb.com/news/movie/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3002.76 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    print(f'status code: {response.status_code}')
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        news_items = soup.find_all('div', class_='ipc-list-card--border-line')
        for item in news_items:
            # print(item)
            title = item.find('a', class_='ipc-link ipc-link--base sc-85efd06-2 hOgzsN') # .text.strip()
            description = item.find('div', class_='ipc-html-content-inner-div')
            image = item.find('img', class_='ipc-image')
            
            if title:
                external_link = title['href']
                title = title.text.strip()
            else:
                title = 'No Title Found'
                external_link = 'No Link Found'

            if description:
                description = description.text.strip()
            else:
                description = 'No Description Found'

            if image:
                image = image['src']
                image_name = f'{uuid.uuid4()}.jpg'
                image_path = f'Images/{image_name}'
                download_image.delay(image, 'Images', image_name)
                image = image_path
            else:
                image = 'No Image Found'


            news = {
                'title': title,
                'description': description,
                'image': image,
                'external_link': external_link
            }
            News.objects.create(**news)

            # link = item.find('a', class_='ipc-link ipc-link--base sc-85efd06-2 hOgzsN')['href']
            # image = item.find('img', class_='ipc-image')['src']

            # print(f'Title: {title}')
            # print(f'Description: {description}')
            # # print(f'Link: {link}')
            # print(f'Image: {image}')
            # print(f'External Link: {external_link}')
            # print('---------------------------------')
    else:
        print(f'Failed to retrieve the page. Status code: {response.status_code}')


if __name__ == '__main__':
    scrape_imdb_news()