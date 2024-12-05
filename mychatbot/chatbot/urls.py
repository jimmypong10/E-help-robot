from django.urls import path
from chatbot import views,help_input
from .help_input import help_input
from .chatbotDoc import chatbotDoc
from .chatbot import chatbot
from .membercenter import membercenter

urlpatterns = [
   path('',views.login,name="login"),
   path("chatbot", chatbot ,name='chatbot'),
   path("chatbotDoc", chatbotDoc ,name='chatbotDoc'),
   path("login", views.login ,name='login'),
   path("logout", views.log_out,name='log_out'),
   path('register', views.register, name='register'),
   path("index", views.index, name='index'),
   path("game", views.game, name='game'),
   path('api/help_input/', help_input, name='help_input'),
   path("membercenter", membercenter, name='membercenter'),
]
