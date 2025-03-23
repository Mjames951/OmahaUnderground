from django.urls import path
from . import chatviews as views

urlpatterns = [
    path('', views.chat, name='chat'),
    path('<channelname>/<int:load>/', views.channel, name="channel"),
    path('report/', views.nothin, name="chatreport"),
    path('report/<postid>/', None)
]