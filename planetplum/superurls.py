from django.urls import path
from . import superviews as views

urlpatterns = [
    path('', views.superuser, name='superuser'),
    path('addband/', views.addBand, name='s_addband'),
    path('editband/<bandname>/', views.editBand, name="s_editband"),
    path('addlabel/', views.addLabel, name='s_addlabel'),
    path('editlabel/<labelname>/', views.editLabel, name='s_editlabel'),
    path('addshow/', views.addShow, name='s_addshow'),
    path('editshow/<showid>/', views.editShow, name='s_editshow'),
    path('addvenue/', views.addVenue, name='s_addvenue'),
    path('editvenue/<venuename>/', views.editVenue, name='s_editvenue'),

    path('approve/band/<bandname>/', views.approveBand, name='approveband'),
    path('approve/label/<labelname>/', views.approveLabel, name='approvelabel'),
    path('approve/show/<showid>/', views.approveShow, name='approveshow'),
]