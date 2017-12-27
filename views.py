from django.contrib.auth import (
                      authenticate,
                      get_user_model,
                      login,
                      logout,
                      )
from django.shortcuts import render, redirect

from .forms import UserLoginForm, UserRegisterForm

from django.http import HttpResponse

from django.views.generic import TemplateView
import plotly.dashboard_objs as dashboard
import IPython.display
from IPython.display import Image
 
def home(request):
 
    return render(request, 'loginapp/home.html', {})
    
    
def dashboard(request, username):
    username = username.objects.filter(username=username)
    
    return render(request, 'loginapp/dashboard.html', {"username": username})   
    

def login_view(request):
    print(request.user.is_authenticated())
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user == None:
            return HttpResponse('User Doesnt exists')
        elif user.is_authenticated():
#            login(request, user)
            return render(request, 'loginapp/dashboard.html', {"username": user})
#            print(request.user.is_authenticated())
   

    return render(request, 'loginapp/login.html', {"form": form})
    
def register_view(request):    
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        user = authenticate(username=user.username, password=password)
        login(request, user)
        print(request.user.is_authenticated())
    return render(request, 'loginapp/login.html', {"form": form})
    
    
def logout_view(request):    
    form = UserRegisterForm(request.POST or None)
    return render(request, 'loginapp/login.html', {"form": form})
# Create your views here.
