from django.urls import path
from . import superviews as views

urlpatterns = [
    path('addchannel/', views.addChannel, name="s_addchannel"),
    path('addchannelsection/', views.addChannelSection, name="s_addchannelsection"),
]