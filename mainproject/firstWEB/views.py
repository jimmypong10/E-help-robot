from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import cal
from .models import Dialogue
import random
import string
import os
from .forms import DialogueForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView,TemplateView
from django.contrib import auth
from .forms import RegisterForm
from .forms import DoctorForm
from .forms import PatientForm
# Create your views here.


def index(request):
    return render(request,'index.html')

def Calpage(request):
    return render(request,'cal.html')

def cals(request):
    if request.POST:
        va=request.POST["ValueA"]
        vb=request.POST["ValueB"]
        result=int(va)+int(vb)

        cal.objects.create(value_a=va, value_b=vb, result=result)
        return render(request,'result.html',context={'data':result})
    else:
        return HttpResponse('no number')   
    



def sign_up(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login') 
    context = {
        'form': form
    }
    return render(request, 'register.html', context)

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/index')
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/index')
    else:
        return render(request, 'login.html', locals())

def log_out(request):
    auth.logout(request)
    return HttpResponseRedirect('/index')

def doctor_form_view(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            
            form.save()
            return redirect('/index') 
    else:
        form = DoctorForm()
    return render(request, 'doctor.html', {'form': form})

def patient_form_view(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            
            form.save()
            return redirect('/index') 
    else:
        form = PatientForm()
    return render(request, 'patient.html', {'form': form})
