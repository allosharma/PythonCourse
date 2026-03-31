from django.shortcuts import render, redirect
from home.models import Pizza, Order

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
    order = Order.objects.get(order_id=order_id)
    context = {
        'order': order }
    return render(request, 'order.html', context)

def order_pizza(request, pizza_id):
    pizza = Pizza.objects.get(id=pizza_id)
    Order.objects.create(
        pizza=pizza,
        user = request.user,
        amount = pizza.price
    )
    return redirect('/')
