from django.urls import path
from . import views
from users import userviews
urlpatterns = [
    #user urls
    path('register/', userviews.register, name='register'),
    path('user/<username>/', userviews.userProfile, name='userProfile'),
    path('editUserProfile/', userviews.editUserProfile.as_view(), name='editUserProfile'),

    path('', views.index, name='index'),
    path('feedback/', views.feedback, name='feedback'),
    path('about/', views.about, name='about'),
    path('bands/', views.bands.as_view(), name='bands'),
]