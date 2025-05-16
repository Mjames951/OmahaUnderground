from django.urls import path
from . import superviews as views

urlpatterns = [
    path('', views.contribute, name="contribute"),
    path('super/', views.superuser, name='superuser'),

    path('bandlinks/<bandid>/', views.bandlinks, name='bandlinks'),

    path('addshow/', views.addShow, name='s_addshow'),
    path('editshow/<showid>/', views.editShow, name='s_editshow'),

    path('editcommsec/', views.commSecList, name='s_commseclist'),    
 
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

    path('add/<modelname>/<parentid>/', views.addModel, name='addmodelparent'),
    
    path('add/<modelname>/', views.addModel, name='addmodel'),
    path('edit/<modelname>/<id>/', views.editModel, name='editmodel'),
]