from django.urls import path
from . import superviews as views

urlpatterns = [
    path('', views.contribute, name="contribute"),
    path('super/', views.superuser, name='superuser'),

    path('addband/', views.addBand, name='s_addband'),
    path('editband/<bandname>/', views.editBand, name="s_editband"),

    path('addlabel/', views.addLabel, name='s_addlabel'),
    path('editlabel/<labelname>/', views.editLabel, name='s_editlabel'),

    path('addshow/', views.addShow, name='s_addshow'),
    path('editshow/<showid>/', views.editShow, name='s_editshow'),

    path('addvenue/', views.addVenue, name='s_addvenue'),
    path('editvenue/<venuename>/', views.editVenue, name='s_editvenue'),

    path('addannouncement/', views.addAnnouncement, name='s_addannouncement'),
    path('editannouncement/<announcementid>/', views.editAnnouncement, name='s_editannouncement'),

    path('addcommlink/', views.addCommlink, name='s_addcommlink'),
    path('editcommlink/<commlinkid>/', views.editCommLink, name='s_editcommlink'),
    path('addcommsec/', views.addCommSec, name='s_addcommsec'),
    path('editcommsec/', views.commSecList, name='s_commseclist'),    
    path('editcommsec/<sectionid>/', views.editCommSec, name='s_editcommsec'),

    path('approve/band/<bandname>/', views.approveBand, name='approveband'),
    path('approve/label/<labelname>/', views.approveLabel, name='approvelabel'),
    path('approve/show/<showid>/', views.approveShow, name='approveshow'),
]