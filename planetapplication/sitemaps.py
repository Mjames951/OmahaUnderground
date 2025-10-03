from django.contrib.sitemaps import Sitemap
from planetplum.models import Band, Venue, Label, Show
from chat.models import Root
from django.urls import reverse

class StaticSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'
    
    def items(self):
        return ["index", 'explore', 'community', 'shows', 'feedback', 'about', 'labels', 
                'venues', 'announcements', 'bands', 'chat', 'register', 'login']
    def location(self, item):
        return reverse(item)
    
class BandSitemap(Sitemap):
    def items(self):
        return Band.objects.filter(approved=True)
    
class LabelSitemap(Sitemap):
    def items(self):
        return Label.objects.filter(approved=True)
    
class VenueSitemap(Sitemap):
    def items(self):
        return Venue.objects.all()
    
class ShowSitemap(Sitemap):
    def items(self):
        return Show.objects.filter(approved=True)
    
class ChannelSitemap(Sitemap):
    def items(self):
        return Root.objects.all()