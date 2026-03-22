from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
from accounts.emailer import sendOtpToEmail
from django.core.cache import cache

User = get_user_model()

@login_required(login_url='/login/')
def home(request):
    return render(request, 'home.html')



def login_page(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')

        if cache.get(phone_number):
            data = cache.get(phone_number)
            data['count'] += 1
            if data['count'] >= 3:
                cache.set(phone_number, data, 60 * 5)
                messages.error(request, 'You have reached the maximum login attempts. Please try again later.')
                return redirect('login')
            cache.set(phone_number, data, 60 * 1)

        if not cache.get(phone_number):
            data = {
                'phone_number': phone_number,
                'count': 1
            }
            cache.set(phone_number, data, 60 * 1)

        user_obj = User.objects.filter(phone_number=phone_number)
        if not user_obj.exists():
            return redirect('login')
        email = user_obj[0].email
        otp = random.randint(100000, 999999)
        user_obj = user_obj.first()
        user_obj.otp = otp
        user_obj.save()
        print(f'Your OTP is {otp} and email is {email} and phone number is {phone_number}')
        subject = 'OTP Verification'
        message = f'Your OTP is {otp}'

        sendOtpToEmail(email,
                       subject,
                       message)
        return redirect('check_otp', user_id=user_obj.id)

    return render(request, 'login.html')


def check_otp(request, user_id):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user_obj = User.objects.get(id=user_id)

        if str(user_obj.otp) == str(otp):
            user_obj.is_verified = True
            user_obj.save()
            login(request, user_obj)            
            return redirect('home')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, 'checkotp.html')

    return render(request, 'checkotp.html')