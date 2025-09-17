from django.urls import path
from . import userviews

urlpatterns = [
    # account
    path('register/', userviews.register, name='register'),


    # user
    path('profile/<username>/', userviews.userProfile, name='userprofile'),
    path('editUserProfile/', userviews.editUserProfile, name='edituserprofile'),
    path('editUserColors/', userviews.editUserColors, name='editusercolors'),
]