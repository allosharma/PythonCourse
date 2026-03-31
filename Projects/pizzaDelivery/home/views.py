from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from home.models import Pizza, Order
from home.models import order_mapper

# Create your views here.
def index(request):
    pizzas = Pizza.objects.all()
    orders = Order.objects.all()
    context = {
        'pizzas': pizzas,
        'orders': orders
    }
    return render(request, 'index.html', context)


def order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    step_order = list(order_mapper.keys())
    context = {
        'order': order,
        'progress_value': order_mapper.get(order.status, 0),
        'step_order': step_order,
        'current_step_index': step_order.index(order.status) if order.status in step_order else -1,
        }
    return render(request, 'order.html', context)


def order_status(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    data = Order.give_order_details(order_id)
    return JsonResponse(data)

def order_pizza(request, pizza_id):
    pizza = Pizza.objects.get(id=pizza_id)
    Order.objects.create(
        pizza=pizza,
        user = request.user,
        amount = pizza.price
    )
    return redirect('/')
