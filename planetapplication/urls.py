from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contribute/', include("planetplum.superurls")),
    path('user/', include("users.userurls")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('chat/', include("chat.chaturls")),
    path('chat/superuser/', include("chat.superurls")),

    #put last so /band takes you to the proper page
    path('', include("planetplum.urls")),
]


urlpatterns += [
    path('tz_detect/', include('tz_detect.urls')),
]