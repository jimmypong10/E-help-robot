from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib import auth 
from django.contrib.auth.models import User
from .models import Chat
import openai
from django.utils import timezone
from django.conf import settings
import requests
from .utils import find_patient_id_by_identifier
from .models import PatientRecord
from django.contrib import messages
from .his_utils import *

# from fhirclient.models.patient import Patient
# from fhirclient.models.fhirdate import FHIRDate
# from fhirclient.models.humanname import HumanName
# from .fhir_utils import get_fhir_client
# from fhirclient import client
# Create your views here.

openai.api_type = "azure"
openai.api_version = "2023-05-15"
openai.api_key = "1a3aff77e6e24a3198098b7846e0342d"
openai.api_base = "https://001-openai.openai.azure.com/"
server_url = "http://localhost:8080/fhir"
def ask_openai(message):
    response = openai.ChatCompletion.create(
        engine="40",  
        messages=[
            {"role": "system", "content": "You are a medical educational assistant. "
                        "Provide accurate and easy-to-understand medical information. "
                        "Remember to advise users to consult with healthcare professionals for medical advice."},
            {"role": "user", "content": message},
        ],
        max_tokens=150,
    )
    
    return response['choices'][0]['message']['content'].strip()
# Create your views here.
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats})

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
            return redirect('detail')
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



def link_hospital(request):
    
    if request.method == 'GET':
        identifier_value = request.user
        identifier, patient_id = find_patient_id_by_identifier(server_url, identifier_value)

        if patient_id:
            patient_record = PatientRecord.objects.create(identifier=identifier, patient_id=patient_id)
            messages.success(request, '連接成功')
        else:
            messages.error(request, '無病患資料')

    return redirect('index')


def link_detail(request):
    if request.method == 'GET':
        identifier_value = request.user.username  # 假設使用者帳號是身分證號
        identifier, patient_id = find_patient_id_by_identifier('http://localhost:8080/fhir', identifier_value)

        if patient_id:
            records = get_patient_records('http://localhost:8080/fhir', patient_id)
            if records:
                save_patient_records(identifier, patient_id, records)
                messages.success(request, '病歷資料已成功寫入資料庫')
            else:
                messages.error(request, '無新增病歷資料')
        else:
            messages.error(request, '無病患資料')

    return redirect('link')

  