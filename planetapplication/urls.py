from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('superuser/', include("planetplum.superurls")),
    path('user/', include("users.userurls")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('chat/', include("chat.chaturls")),
    
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}), #serve media files when deployed
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root':settings.STATIC_ROOT}), #serve static files when deployed

    #put last so /band takes you to the proper page
    path('', include("planetplum.urls")),
]