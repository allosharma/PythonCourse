from django.shortcuts import render
from likes.kafka_producer import send_like_event

# Create your views here.
from django.http.response import JsonResponse
from likes.models import Post


# Important point to remeber to run this app is to first run kafka server, then kafka Consumer, then app
# Consumer: (.env) PS C:\Users\asharma\Documents\Alok\PythonCourse\Projects\likeCounter> python manage.py kafka_consumer
# Then run the app
# Then run the locust file: (.env) PS C:\Users\asharma\Documents\Alok\PythonCourse\Projects\likeCounter> locust
# test with numbers of users and request per user in locust  at: localhost:8089
def post_like(request, post_id):
    send_like_event(post_id)
    # post = Post.objects.get(id=post_id)
    # post.like += 1
    # post.save()
    return JsonResponse({
        'status': True,
        'message': 'Like incremented successfully'
    })