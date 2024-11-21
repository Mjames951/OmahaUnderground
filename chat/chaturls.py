from django.urls import path
from . import chatviews as views

urlpatterns = [
    path('', views.chat, name='chat'),
    path('<channel>/', views.channel, name="channel")
]