from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('announcements/', views.announcements, name='announcements'),
    path('community/', views.community, name='community'),
    path('feedback/', views.feedback, name='feedback'),
    

    # EXPLORE PAGES
    path('shows/', views.shows.as_view(), name='shows'),
    path('shows/<slug>', views.showpage, name='showpage'),

    path('labels/', views.labels, name='labels'),
    path('labels/<slug>/', views.labelpage, name='labelpage'),

    path('venues/', views.venues, name='venues'),
    path('venues/<slug>', views.venuepage, name='venuepage'),

    path('bands/', views.bands, name='bands'),
    #last so all the other pages come up first
    path('<slug>', views.bandpage, name="bandpage"),
]