from django.shortcuts import render, redirect
from django.contrib import auth 
from django.contrib.auth.models import User
from .utils import find_patient_id_by_identifier
from .models import PatientRecord
from django.contrib import messages

# from fhirclient.models.patient import Patient
# from fhirclient.models.fhirdate import FHIRDate
# from fhirclient.models.humanname import HumanName
# from .fhir_utils import get_fhir_client
# from fhirclient import client
# Create your views here.
def index(request):
    return render(request,"index.html")

def register(request):
    if request.method == "POST":
        username =request.POST["username"]
        email =request.POST["email"]
        password1 =request.POST["password1"]
        password2 =request.POST["password2"]
        if password1 == password2:
             try:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                auth.login(request,user)
                return redirect('index')
             except:
                 error_msg ="註冊失敗"
                 return render(request, 'register.html',{'error_message':error_msg})
        else:
            error_msg ="密碼輸入錯誤"
            return render(request, 'register.html',{'error_message':error_msg})
    return render(request, 'register.html')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request,username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            error_msg ="登入失敗"
            return render(request, 'login.html',{'error_message':error_msg})
    else:
        return render(request, 'login.html')

def log_out(request):
    auth.logout(request)
    return redirect('login')

def game(request):
    return render(request,"game.html")

def shop(request):
    return render(request,"product.html")