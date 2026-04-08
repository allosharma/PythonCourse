from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_POST


def registration(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('phone_number', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        if not all([first_name, last_name, username, email, password]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('registration')

        user_exists = User.objects.filter(
            Q(username=username) | Q(email__iexact=email)
        )

        if user_exists.exists():
            messages.error(request, 'A user with this phone number or email already exists.')
            return redirect('registration')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
        )

        login(request, user)
        messages.success(request, 'Registration successful.')
        return redirect('home')

    return render(request, 'registration.html')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('phone_number', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('home')

        messages.error(request, 'Invalid phone number or password.')
        return redirect('login')

    return render(request, 'login.html')


@require_POST
def logoutPage(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('home')
