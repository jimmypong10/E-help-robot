from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
from django.utils import timezone
from django.conf import settings
from django import forms
from .models import Chat3
from django.http import HttpResponseRedirect
import base64
import ollama

class botform(forms.Form):  #表單接收
    message = forms.CharField(max_length=50,label='',widget=forms.TextInput(attrs={'class': 'form-control message-input','placeholder': '輸入訊息...'}))
"""
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


def encode_image(image_path):
  with open(image_path, "rb") as image_file:   #輸入需提供檔案路徑
    return base64.b64encode(image_file.read()).decode('utf-8')
"""
def ask_breeze(message):
    #使用ollama模型，進行對話
    prompt={"You are a medical educational assistant.",
            "Provide accurate and easy-to-understand medical information. ",
            "Remember to advise users to consult with healthcare professionals for medical advice."} #提示詞
    response = ollama.chat(
    model='ycchen/breeze-7b-instruct-v1_0',
    
    messages=[
        {
            'role': 'prompt','content':prompt,
            'role': 'user', 'content': message}])
    """print(response)
    print(type(response))"""
    return response['message']['content'].strip()

def chatbot3(request):
    chats = Chat3.objects.filter(user=request.user)
    if request.method == "POST":
        form = botform(request.POST)
        if form.is_valid():
            message = request.POST.get('message')
            response = ask_breeze(message)
        else:
            print("error")
            print(form.errors.as_data())
        """
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        """
        return JsonResponse({'message': message, 'response': response})
    else:
        form = botform()
    return render(request, 'chatbot3.html', {'chats': chats,'form':form})

