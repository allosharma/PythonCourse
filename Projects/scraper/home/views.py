from django.shortcuts import render
from django.http import JsonResponse
from scraper.script import scrape_imdb_news
from home.models import News
from home.task import add


# Create your views here.

def run_scraper(request):
    scrape_imdb_news()
    return JsonResponse({
        'status': 'success',
        'message': 'Scraper is running in the background.'
    })

def index(request):
    results = add.delay(10, 5)
    print(f'Results: {results}')
    return render(request, 'index.html', context={
        'news': News.objects.all()
    })
