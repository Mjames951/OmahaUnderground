from django.urls import path
from . import superviews as views

urlpatterns = [
    path('', views.superuser, name='superuser'),
    path('addband/', views.addBand, name='s_addband'),
    path('editband/<bandname>/', views.editBand, name="s_editband"),
    path('addshow/', views.addShow, name='s_addshow'),
]