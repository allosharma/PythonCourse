from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import Sum, Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import logging
logger = logging.getLogger(__name__)


def registration(request):

    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_exists = User.objects.filter(
            Q(username=username) | Q(email=email)
        )

        if user_exists.exists():
            messages.error(request, 'Error: Username or Email already exists.')
            return redirect('registration')

        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email
        )

        user.set_password(password)  # password hashed here
        user.save()
        
        login(request, user)
        messages.success(request, 'Success: Registration successful!')
        return redirect('index')

    return render(request, 'registration.html')

def loginPage(request):
    
    logger.debug("Login Page - This is a debug message")
    logger.info("Login Page - This is an info message")
    logger.warning("Login Page - This is a warning message")
    logger.error("Login Page - This is an error message")
    logger.critical("Login Page - This is a critical message")

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect('index')

        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')


def logoutPage(request):
    logout(request)
    messages.success(request, "Logout successful")
    print(request.user)
    return redirect('login')


@login_required(login_url='login')
def index(request):
    print(request.user.is_authenticated, request.user)
    if request.method == 'POST':
        # Handle form submission for adding a new transaction
        description = request.POST.get('description')
        amount = request.POST.get('amount')

        # print(f'Amount Type: {type(amount)}')

        try:
            amount = float(amount)
        except ValueError:
            messages.error(request, 'Amount must be a number.')
            return redirect('index')

        if description and amount:
            messages.success(request, 'Transaction added successfully!')
            
            # Process the transaction (e.g., save to database)
            Transaction.objects.create(
                created_by=request.user, 
                description=description, 
                amount=amount)
            
            return redirect('index')  # Redirect to the same page to show the updated transaction list
        
        else:
            messages.error(request, 'Please provide both description and amount.')
            return redirect('index')
        

    context = {
        'History': Transaction.objects.filter(created_by=request.user),  # Fetch all transactions ordered by creation date (using meta class ordering)
        'Balance': Transaction.objects.filter(created_by=request.user).aggregate(balance = Sum('amount'))['balance'] or 0,
        'Income': Transaction.objects.filter(created_by=request.user, amount__gt=0).aggregate(Income = Sum('amount'))['Income'] or 0,
        'Expense': Transaction.objects.filter(created_by=request.user, amount__lt=0).aggregate(Expense = Sum('amount'))['Expense'] or 0,
    }
    # print(context)
    return render(request, 'index.html', context)


@login_required(login_url='login')
def deleteTransaction(request, uuid):
    Transaction.objects.filter(uuid=uuid).delete()    
    return redirect('index')
