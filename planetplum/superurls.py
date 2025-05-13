from django.urls import path
from . import superviews as views

urlpatterns = [
    path('', views.contribute, name="contribute"),
    path('super/', views.superuser, name='superuser'),

    path('editband/<bandname>/', views.editBand, name="s_editband"),

    path('editlabel/<labelname>/', views.editLabel, name='s_editlabel'),

    path('addshow/', views.addShow, name='s_addshow'),
    path('editshow/<showid>/', views.editShow, name='s_editshow'),

    path('editvenue/<venuename>/', views.editVenue, name='s_editvenue'),

    path('addannouncement/', views.addAnnouncement, name='s_addannouncement'),
    path('editannouncement/<announcementid>/', views.editAnnouncement, name='s_editannouncement'),

    path('editcommlink/<commlinkid>/', views.editCommLink, name='s_editcommlink'),
    path('addcommsec/', views.addCommSec, name='s_addcommsec'),
    path('editcommsec/', views.commSecList, name='s_commseclist'),    
    path('editcommsec/<sectionid>/', views.editCommSec, name='s_editcommsec'),

    path('approve/band/<bandname>/', views.approveBand, name='approveband'),
    path('approve/label/<labelname>/', views.approveLabel, name='approvelabel'),
    path('approve/show/<showid>/', views.approveShow, name='approveshow'),

    path('messageremove/<reportid>/', views.removeMessage, name='removemessage'),
    path('messagedismiss/<reportid>/', views.dismissMessage, name='dismissmessage'),

    path('delete/<model>/<id>/', views.deleteInstance, name='delete'),
    path('delete/restrict', views.restrict, name='restrict'),

    path('usermanage/<usecase>/<id>/', views.userManage, name='usermanage'),
    path('usermanage/<usecase>/<id>/<username>/add', views.userManageAddUser, name='usermanageadd'),
    path('usermanage/<usecase>/<id>/<username>/remove', views.userManageRemoveUser, name='usermanageremove'),

    
    path('add/<modelname>/', views.addModel, name='addmodel'),
    
]