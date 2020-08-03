"""hrportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from . import views

urlpatterns = [
    path('interviewer-list/', views.InterviewerList.as_view(), name="InterviewerList"),
    path('candidate-list/', views.CandidateList.as_view(), name="CandidateList"),
    path('register-interviewer/', views.RegisterInterviewer.as_view(), name="Registration"),
    path('register-candidate/', views.RegisterCandidate.as_view(), name="Registration"),
    path('login/', views.UserLogin.as_view(), name="UserLogin"),
    path('book-slot/', views.CreateSlot.as_view(), name="CreateSlot"),
    path('get-availability/', views.GetAvailability.as_view(), name="GetAvailability"),
]
