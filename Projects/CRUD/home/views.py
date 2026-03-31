from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Feedback
from django.http import JsonResponse
import json

# Create your views here.

def product_list(request):
    products = Product.objects.all().values('id', 'name', 'price', 'description', 'created_at')
    return JsonResponse(list(products), safe=False)


def get_product_details(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        data = {
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'description': product.description,
            'created_at': product.created_at
        }
        return JsonResponse(data, safe=False)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    
@csrf_exempt
def submit_feedback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            message = data.get('message')
            
            if not name or not email or not message:
                return JsonResponse({'error': 'All fields are required'}, status=400)

            # Save feedback in the database
            feedback = Feedback.objects.create(name=name, email=email, message=message)
            return JsonResponse({'message': 'Feedback submitted successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)