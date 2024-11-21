from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('feedback/', views.feedback, name='feedback'),
    path('about/', views.about, name='about'),
    path('bands/', views.bands.as_view(), name='bands'),


    path('<bandname>', views.bandpage, name="bandpage"),
]