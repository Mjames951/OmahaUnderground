from django.urls import path
from . import superviews as views

urlpatterns = [
    path('addchannel/', views.addChannel, name="s_addchannel"),
    path('addchannelsection/', views.addChannelSection, name="s_addchannelsection"),
    path('editchannel/<channelid>/', views.editChannel, name="s_editchannel"),
    path('editchannelsectoin/<sectionid>/', views.editChannelSection, name="s_editchannelsection"),
    path('chatlist', views.chatList, name="s_chatlist"),
]