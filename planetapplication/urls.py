from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from .sitemaps import *
from django.conf import settings
from django.conf.urls.static import static

sitemaps = {
    "static": StaticSitemap,
    "bands": BandSitemap,
    "labels": LabelSitemap,
    "shows": ShowSitemap,
    "venues": VenueSitemap,
    "channels": ChannelSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contribute/', include("planetplum.superurls")),
    path('user/', include("users.userurls")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('chat/', include("chat.chaturls")),

    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),

    path('tz_detect/', include('tz_detect.urls')),

    #put last so /band takes you to the proper page
    path('', include("planetplum.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)