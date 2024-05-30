from django.urls import path
from chatbot import views

urlpatterns = [
   path('',views.index,name="index"),
   path("chatbot", views.chatbot ,name='chatbot'),
   path("login", views.login ,name='login'),
   path("logout", views.log_out,name='log_out'),
   path('register', views.register, name='register'),
   path("index/", views.index, name='index'),
]
