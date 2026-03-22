from typing import Any
from django.http import HttpResponseForbidden
from home.models import Store


Allowed_IPs = ['127.0.0.1']

class IPBlockingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def __call__(self, request):
        ip = self.get_client_ip(request)
        print(f'Client IP: {ip}')  # Add this line to print the client IP (ip)
        if ip not in Allowed_IPs:
            return HttpResponseForbidden('Access Denied')

        response = self.get_response(request)
        return response
    
class checkBMPHeader:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        clientHeaders = request.headers
        print(f'Client Header: {clientHeaders}')  # Add this line to print the client IP (ip)
        if 'bmp' not in clientHeaders:
            return HttpResponseForbidden('BMP Header Not Found')
        elif not Store.objects.filter(store_id=clientHeaders['bmp']).exists():
                return HttpResponseForbidden('BMP Header Not Matching')

        response = self.get_response(request)
        return response