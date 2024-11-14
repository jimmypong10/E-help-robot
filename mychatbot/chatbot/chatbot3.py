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
    return response['message']['content'].strip()

def chatbot3(request):
    chats = Chat3.objects.filter(user=request.user)
    if request.method == "POST":
        print("already_executed="+str(request.session["already_executed"]))
        request.session["already_executed"]=False
        initialize(request)
        form = botform(request.POST)
        if form.is_valid():
            message = request.POST.get('message')
            response = handle_user_input(message,collection)
        else:
            print("error")
            print(form.errors.as_data())
        chat = Chat3(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        
        return JsonResponse({'message': message, 'response': response})
    else:
        form = botform()
    return render(request, 'chatbot3.html', {'chats': chats,'form':form})

import chromadb  # 導入chromadb庫，用於數據存儲和查詢
import pandas as pd  # 導入pandas庫，用於數據分析和處理
import requests

def initialize(request):
    #檢查'session_state'（會話狀態）中是否已有'already_executed'這個變量
    #這個變量用來檢查是否已經進行過一次資料庫初始化操作
    if 'already_executed' not in request.session:
        request.session["already_executed"]=False  # 若不存在，則設置為False

    #如果'already_executed'為False，表示還未初始化過資料庫
    if request.session["already_executed"]==False:
        setup_database(request)  # 呼叫setup_database函數來進行資料庫的設置和數據加載
#定義設置資料庫的函數
def setup_database(request):
    client = chromadb.Client()  # 創建一個chromadb的客戶端，用於與資料庫交互
    file_path = 'mychatbot/RAG_data/demodocs.xlsx'# 指定Excel文件的路徑和名稱
    documents = pd.read_excel(file_path, header=None)  # 使用pandas讀取Excel文件

    #使用chromadb客戶端創建或獲取名為'demodocs'的集合
    #嘗試把collection改成全域變數
    global collection 
    collection = client.get_or_create_collection(name="demodocs")

    #遍歷從Excel文件中讀取的數據，每一行代表一條記錄
    for index, content in documents.iterrows():
        response = ollama.embeddings(model="mxbai-embed-large", prompt=content[0])  # 通過ollama生成該行文本的嵌入向量
        collection.add(ids=[str(index)], embeddings=[response["embedding"]], documents=[content[0]])  # 將文本和其嵌入向量添加到集合中
    request.session["already_executed"] = True  # 設置'already_executed'為True，表示已完成初始化
    #print(collection)
    #request.session["collection"]=collection# 將集合保存在會話狀態中，供後續使用    

#定義創建新chromadb客戶端的函數，每次需要時創建新的連接
def create_chromadb_client():
    return chromadb.Client()  # 返回一個新的chromadb客戶端實例

def handle_user_input(user_input, collection):
    #print("runned handle user")
    #print(collection)
    response = ollama.embeddings(prompt=user_input, model="mxbai-embed-large")  # 生成用戶輸入的嵌入向量
    results = collection.query(query_embeddings=[response["embedding"]], n_results=3)  # 在集合中查詢最相關的三個文件
    data = results['documents'][0]  # 獲取最相關的文件
    #print(data)
    prompt={"You are a medical educational assistant.",
        f"Provide accurate and easy-to-understand medical informationUsing this data: {data}. ",
        "Remember to advise users to consult with healthcare professionals for medical advice."} #提示詞
    response = ollama.chat(
    model='ycchen/breeze-7b-instruct-v1_0',
    
    messages=[
        {
            'role': 'prompt','content':prompt,
            'role': 'user', 'content': user_input}])
    return response['message']['content'].strip()

