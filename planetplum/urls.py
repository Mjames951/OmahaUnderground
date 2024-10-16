from django.urls import path
from . import views
from . import secretViews
urlpatterns = [
    path('', views.index, name='index'),

    path('secret', secretViews.index, name='index'),
]