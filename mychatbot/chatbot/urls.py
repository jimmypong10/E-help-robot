from django.urls import path
from chatbot import views

urlpatterns = [
   path('',views.chatbot,name="chatbot"),
   path("login", views.login ,name='login'),
   path("logout", views.log_out,name='log_out'),
   path('register', views.register, name='register'),

]
