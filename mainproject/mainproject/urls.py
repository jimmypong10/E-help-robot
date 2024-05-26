"""
URL configuration for mainproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from firstWEB import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index,name='index'),
    path("index/", views.index,name='index'),
    path("calpage/", views.Calpage),
    path("cal/", views.cals),
    #  path('dialogue/', views.dialogue_view),
    # path('sign_up/', views.SignUpView.as_view(), name = "sign_up"),
    path("login/", views.login ,name='login'),
    path("logout/", views.log_out,name='log_out'),
    path('/register/', views.sign_up, name='register'),
    path('doctor/', views.doctor_form_view, name='doctor'),
    path('patient/', views.patient_form_view, name='patient'),
]