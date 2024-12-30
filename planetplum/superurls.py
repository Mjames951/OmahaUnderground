from django.urls import path
from . import superviews as views

urlpatterns = [
    path('', views.superuser, name='superuser'),
    path('addband/', views.addBand, name='s_addband'),
    path('editband/<bandname>/', views.editBand, name="s_editband"),
    path('addlabel/', views.addLabel, name='s_addlabel'),
    path('editlabel/<labelname>/', views.editLabel, name='s_editlabel'),
    path('addshow/', views.addShow, name='s_addshow'),
    path('addvenue/', views.addVenue, name='s_addvenue'),
    path('editvenue/', views.editVenue, name='s_editvenue'),
]