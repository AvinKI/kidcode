from django.shortcuts import render , HttpResponse , redirect
from .models import *
from .forms import ContactForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

import logging
logger = logging.getLogger(__name__)

def login_student(request  ):
    if request.method == "POST":
        user_name = request.POST.get("username")
        print(user_name)
        user_password = request.POST.get("password")
        print(user_password)

        logger.info(f"Trying to authenticate user: {user_name}")
        user = authenticate(request, username=user_name, password=user_password)
        if user is not None:
            logger.info("Authentication successful")
            login(request, user)
            return redirect('dashboard_student')
        else:
            logger.warning("Authentication failed")
            messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
    return render(request, "login.html")




def home(request):
    slider = Slide.objects.all()
    supporters = Supporter.objects.all()
    commment = Commment.objects.all()
    return render(request, 'home.html', {'slider': slider, 'supporters': supporters , 'commment':commment})


def about_us(request):
    return render(request,'about-us.html')



def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("پیام شما با موفقیت ذخیره شد. با تشکر!")
    else:
        form = ContactForm()

    return render(request, 'contact-us.html', {'form': form})


def doucument(request):
    return render(request,'doucument.html')

def developers(request):
    return render(request , 'programers.html' )