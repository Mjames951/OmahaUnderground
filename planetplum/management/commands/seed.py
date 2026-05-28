import io
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image

from planetplum.models import Band, Show, Venue, Label

User = get_user_model()

PLACEHOLDER_SIZE = (100, 100)
PLACEHOLDER_COLOR = (102, 102, 255)


def _placeholder_image(name):
    buf = io.BytesIO()
    Image.new("RGB", PLACEHOLDER_SIZE, PLACEHOLDER_COLOR).save(buf, format="JPEG")
    buf.seek(0)
    return ContentFile(buf.read(), name=name)


class Command(BaseCommand):
    help = "Seed the database with an admin user and sample data for local development"

    def handle(self, *args, **options):
        self.admin_email = "admin@localhost"
        self.band_name = "Valley Street"
        self.venue_name = "The Waiting Room"
        self.show_name = "Sick Punk Show"
        self.label_name = "Planet Plum"
        self._seed_admin(self.admin_email)
        self._seed_venue(self.venue_name)
        self._seed_band(self.band_name )
        self._seed_show(self.show_name, self.venue_name, self.band_name)
        self._seed_label(self.label_name)


    def _seed_admin(self, admin_email:str):
        if User.objects.filter(username="admin").exists():
            self.stdout.write("  admin user already exists, skipping")
            return
        User.objects.create_superuser(
            username="admin",
            email="admin_email",
            password="admin",
            admin=True,
            trusted=True,
        )
        self.stdout.write(self.style.SUCCESS("  created admin user  (admin / admin)"))

    def _seed_venue(self, venue_name:str):
        _, created = Venue.objects.get_or_create(
            name=venue_name,
            defaults={"ageRange": "2", "approved": True},
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"  created venue: {venue_name}"))
        else:
            self.stdout.write("  venue already exists, skipping")

    def _seed_label(self, label_name:str):
        if Label.objects.filter(name=label_name).exists():
            self.stdout.write("  label already exists, skipping")
            return
        label = Label(name=label_name, approved=True)
        label.image.save("seed_label.jpg", _placeholder_image("seed_label.jpg"), save=True)
        self.stdout.write(self.style.SUCCESS(f"  created label: {label_name}"))


    def _seed_band(self, band_name):
        
        if Band.objects.filter(name=band_name).exists():
            self.stdout.write("  band already exists, skipping")
            return
        band = Band(name=band_name, approved=True)
        band.image.save("seed_band.jpg", _placeholder_image("seed_band.jpg"), save=True)
        self.stdout.write(self.style.SUCCESS(f"  created band: {band_name}"))

    def _seed_show(self, show_name:str, venue_name:str, band_name:str):
        if Show.objects.filter(name=show_name).exists():
            self.stdout.write("  show already exists, skipping")
            return
        venue = Venue.objects.filter(name=venue_name).first()
        contributor = User.objects.filter(username="admin").first()
        show = Show(
            name=show_name,
            date=date.today() + timedelta(days=7),
            venue=venue,
            location=venue_name,
            approved=True,
            contributor=contributor,
        )
        show.image.save("seed_show.jpg", _placeholder_image("seed_show.jpg"), save=True)
        band = Band.objects.filter(name=band_name).first()
        if band:
            show.bands.add(band)
        self.stdout.write(self.style.SUCCESS(f"  created show: {show_name} with band {band_name} at venue {venue_name}"))
