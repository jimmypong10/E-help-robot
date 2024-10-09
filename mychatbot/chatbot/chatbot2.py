from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Chat
import openai
from django.utils import timezone
from django.conf import settings
from django import forms
from .models import Chat2
from .models import picsave
from django.http import HttpResponseRedirect
import base64
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"
openai.api_version = "2023-05-15"
openai.api_key = "1a3aff77e6e24a3198098b7846e0342d"
openai.api_base = "https://001-openai.openai.azure.com/"

class botform(forms.Form):  #表單接收
    textinput = forms.CharField(max_length=50,label='',widget=forms.TextInput(attrs={'class': 'form-control message-input','placeholder': '輸入訊息...'}))
    Imginp = forms.ImageField(required=False,widget=forms.ClearableFileInput(attrs={'class': 'IMGclass'}))

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

def encode_image(image_path):
  with open(image_path, "rb") as image_file:   #輸入需提供檔案路徑
    return base64.b64encode(image_file.read()).decode('utf-8')
  
client = AzureOpenAI( 
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key = os.getenv("AZURE_OPENAI_API_KEY"),
    api_version = "2023-05-15"
)

def ask_openai_image(message,image_path):
    base64_image = encode_image(image_path)
    response =  client.chat.completions.create(
    #engine="40", 
    model="imagetest",
    messages=[
        {"role": "system", "content": "You are a medical educational assistant. "
                        "Provide accurate and easy-to-understand medical information. "
                        "Remember to advise users to consult with healthcare professionals for medical advice."},
        { "role": "user", "content": [  
            { 
                "type": "text", 
                "text": message 
            },
            { 
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        ] } 
    ],
    max_tokens=150
    )
    return response['choices'][0]['message']['content'].strip()

def chatbot2(request):
    chats = Chat2.objects.filter(user=request.user)
    if request.method == "POST":
        form = botform(request.POST, request.FILES)
        if form.is_valid():
            doc = request.FILES.get('Imginp',None)#從表單中抓位於Imginp位置的檔案(把圖片抓出來) 如果沒有圖片會變成none
            if doc!=None:
                imgfile = picsave(image=doc)
                imgfile.save()#前一行指定圖片放在picsave模型 image的位置 然後儲存 會放在images/botinput/
                print("path:",imgfile.image.path)
                message = request.POST.get('textinput')
                response = ask_openai_image(message,imgfile.image.path)
            else:
                message = request.POST.get('textinput')
                response = ask_openai(message)
        else:
            print("error")
            print(form.errors.as_data())
        return JsonResponse({'message': message, 'response': response})
    else:
        form = botform()
    return render(request, 'chatbot2.html', {'chats': chats,'form':form})

