from django.contrib.sitemaps import Sitemap
from planetplum.models import Band, Venue, Label, Show
from chat.models import Root
from django.urls import reverse

class StaticSitemap(Sitemap):
    priority = 1
    changefreq = 'monthly'
    
    def items(self):
        return ['index', 'shows', 'bands', 'venues', 'community', 'chat', 'labels', 'about']
    def location(self, item):
        return reverse(item)
    
class BandSitemap(Sitemap):
    priority = 0.75

    def items(self):
        return Band.objects.filter(approved=True)
    
class LabelSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return Label.objects.filter(approved=True)
    
class VenueSitemap(Sitemap):
    priority = 0.5
    def items(self):
        return Venue.objects.all()
    
class ShowSitemap(Sitemap):
    priority = 0.5 
    def items(self):
        return Show.objects.filter(approved=True)
    
class ChannelSitemap(Sitemap):
    priority=0.5
    def items(self):
        return Root.objects.all()