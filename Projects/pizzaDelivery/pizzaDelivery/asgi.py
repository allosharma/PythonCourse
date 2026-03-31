"""
ASGI config for pizzaDelivery project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
#It's important to import os.environ here, so that the environment variables are loaded before the get_asgi_application is called
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pizzaDelivery.settings')

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from home.consumer import OrderProgress
# from home.consumers import AdminChatConsumer, PublicChatConsumer



django_asgi_app = get_asgi_application()

ws_pattern = [
    path("ws/pizza/<str:order_id>/", OrderProgress.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": django_asgi_app,   # REQUIRED
    "websocket": URLRouter(ws_pattern),  # FIXED
})