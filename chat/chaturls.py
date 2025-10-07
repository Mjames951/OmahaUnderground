from django.urls import path
from . import chatviews as views

urlpatterns = [
    path('', views.chat, name='chat'),
    path('<name>/', views.root, name="root"),
    path('<channelname>/report/<postid>/', views.report, name="chatreport"),
    path('<channelname>/delete/<postid>/', views.delete, name="chatdelete"),

    path('chatlist', views.chatList, name="s_chatlist"),
]