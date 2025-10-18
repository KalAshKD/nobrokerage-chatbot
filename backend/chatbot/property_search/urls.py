from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat_query, name='chat_query'),
    path('', views.chat_interface, name='chat_interface'),
]