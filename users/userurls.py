from django.urls import path
from . import userviews

urlpatterns = [
    #user urls
    path('register/', userviews.register, name='register'),
    path('profile/<username>/', userviews.userProfile, name='userprofile'),
    path('editUserProfile/', userviews.editUserProfile.as_view(), name='edituserprofile'),
    path('editUserColors/', userviews.editUserColors, name='editusercolors'),
]