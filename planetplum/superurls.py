from django.urls import path
from . import superviews as views

urlpatterns = [
    # CONTRIBUTE PAGES
    path('', views.contribute, name="contribute"),

    path('addshow/', views.addShow, name='s_addshow'),
    path('editshow/<showid>/', views.editShow, name='s_editshow'),

    path('bandlinks/<bandid>/', views.bandlinks, name='bandlinks'),  

    path('add/<modelname>/<parentid>/', views.addModel, name='addmodelparent'),
    path('add/<modelname>/', views.addModel, name='addmodel'),
    path('edit/<modelname>/<id>/', views.editModel, name='editmodel'),
    path('delete/<modelname>/<id>/', views.deleteInstance, name='delete'),
    path('delete/restrict', views.restrict, name='restrict'),


    # USER MANAGE PAGES
    path('usermanage/<usecase>/<id>/', views.userManage, name='usermanage'),
    path('usermanage/<usecase>/<id>/<username>/add', views.userManageAddUser, name='usermanageadd'),
    path('usermanage/<usecase>/<id>/<username>/remove', views.userManageRemoveUser, name='usermanageremove'),


    # ADMIN PAGES
    path('editcommsec/', views.commSecList, name='s_commseclist'),  
    
    path('super/', views.superuser, name='superuser'),
    path('approve/<modelname>/<identifier>/', views.approveModel, name='approvemodel'),
    path('messageremove/<reportid>/', views.removeMessage, name='removemessage'),
    path('messagedismiss/<reportid>/', views.dismissMessage, name='dismissmessage'),
]