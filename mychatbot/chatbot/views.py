from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib import auth 
from django.contrib.auth.models import User
from .models import Chat
import openai
from django.utils import timezone
from django.conf import settings
# Create your views here.

openai.api_type = "azure"
openai.api_version = "2023-05-15"
openai.api_key = "1a3aff77e6e24a3198098b7846e0342d"
openai.api_base = "https://001-openai.openai.azure.com/"

def ask_openai(message):
    response = openai.ChatCompletion.create(
        engine="40",  
        messages=[
            {"role": "system", "content": "You are a medical educational assistant. "
                        "Provide accurate and easy-to-understand medical information. "
                        "Remember to advise users to consult with healthcare professionals for medical advice."},
            {"role": "user", "content": message},
        ],
        max_tokens=30,
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
                return redirect('chatbot')
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
            return redirect('chatbot')
        else:
            error_msg ="登入失敗"
            return render(request, 'login.html',{'error_message':error_msg})
    else:
        return render(request, 'login.html')

def log_out(request):
    auth.logout(request)
    return redirect('login')

