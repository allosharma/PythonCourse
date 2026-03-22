from django.shortcuts import render
from django.http import JsonResponse
from home.models import Store

# Create your views here.
def index(request):
    # return render(request, 'index.html')
    store = Store.objects.get(store_id= request.headers.get('bmp'))
    print(request.headers.get('bmp'))
    print(store)

    data = {
        'message': 'Hello, world!',
        'status': 200,
        'data': {
            'store_id': store.store_id,
            'store_name': store.store_name
        }
    }

    return JsonResponse(data)