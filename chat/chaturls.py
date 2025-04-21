from django.urls import path
from . import chatviews as views

urlpatterns = [
    path('', views.chat, name='chat'),
    path('<channelname>/<int:load>/', views.channel, name="channel"),
    path('<channelname>/<int:load>/report/<postid>/', views.report, name="chatreport"),
    path('<channelname>/<int:load>/delete/<postid>/', views.delete, name="chatdelete")
]