from django.urls import path
from . import chatviews as views
from . import superviews

urlpatterns = [
    path('', views.chat, name='chat'),
    path('<name>/', views.root, name="root"),
    path('<channelname>/<int:load>/report/<postid>/', views.report, name="chatreport"),
    path('<channelname>/<int:load>/delete/<postid>/', views.delete, name="chatdelete"),

    path('chatlist', superviews.chatList, name="s_chatlist"),
]