from django.urls import path
from chatbot import views

urlpatterns = [
   path('',views.login,name="login"),
   path("chatbot", views.chatbot ,name='chatbot'),
   path("login", views.login ,name='login'),
   path("logout", views.log_out,name='log_out'),
   path('register', views.register, name='register'),
   path("index/", views.index, name='index'),
   path("game/", views.game, name='game'),
   path("link/", views.link_hospital, name='link'),
   path("detail/", views.link_detail, name='detail'),
   path("tlink/", views.try_link, name='tlink'),
   # path('c_patient/',  views.create_patient_view, name='c_patient'),
   # path('patients/',  views.patients, name='patients'),
]
