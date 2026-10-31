"""
URL configuration for myroomie project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.urls import path

from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('add/', views.room_create, name='room_create'),


    path('update/<int:pk>/', views.room_update, name='room_update'),
    path('delete/<int:pk>/', views.room_delete, name='room_delete'),

    path('room/<int:pk>/',views.room_detail,name='room_detail'),




    path( 'my-rooms/',views.my_rooms,name='my_rooms'),




]