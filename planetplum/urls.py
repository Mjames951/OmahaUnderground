from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shows/', views.shows.as_view(), name='shows'),
    path('shows/<showid>', views.showpage, name='showpage'),
    path('feedback/', views.feedback, name='feedback'),
    path('about/', views.about, name='about'),
    path('bands/', views.bands.as_view(), name='bands'),
    path('labels/', views.labels.as_view(), name='labels'),
    path('labels/<labelname>/', views.labelpage, name='labelpage'),
    path('venues/', views.venues.as_view(), name='venues'),
    path('venues/<venuename>', views.venuepage, name='venuepage'),

    #last so all the other pages come up first
    path('<bandname>', views.bandpage, name="bandpage"),
]