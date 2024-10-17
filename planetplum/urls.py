from django.urls import path
from . import views
from . import secretViews
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('secret', secretViews.index, name='secret_index'),
]