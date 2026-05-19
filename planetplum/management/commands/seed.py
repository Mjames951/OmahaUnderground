import io
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image

from planetplum.models import Band, Show, Venue

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
        self._seed_admin()
        self._seed_venue()
        self._seed_band()
        self._seed_show()

    def _seed_admin(self):
        if User.objects.filter(username="admin").exists():
            self.stdout.write("  admin user already exists, skipping")
            return
        User.objects.create_superuser(
            username="admin",
            email="admin@localhost",
            password="admin",
            admin=True,
            trusted=True,
        )
        self.stdout.write(self.style.SUCCESS("  created admin user  (admin / admin)"))

    def _seed_venue(self):
        venue, created = Venue.objects.get_or_create(
            name="The Waiting Room",
            defaults={"ageRange": "A", "approved": True},
        )
        if created:
            self.stdout.write(self.style.SUCCESS("  created venue: The Waiting Room"))
        else:
            self.stdout.write("  venue already exists, skipping")

    def _seed_band(self):
        if Band.objects.filter(name="Local Test Band").exists():
            self.stdout.write("  band already exists, skipping")
            return
        band = Band(name="Local Test Band", approved=True)
        band.image.save("seed_band.jpg", _placeholder_image("seed_band.jpg"), save=True)
        self.stdout.write(self.style.SUCCESS("  created band: Local Test Band"))

    def _seed_show(self):
        if Show.objects.filter(name="Seed Show").exists():
            self.stdout.write("  show already exists, skipping")
            return
        venue = Venue.objects.filter(name="The Waiting Room").first()
        contributor = User.objects.filter(username="admin").first()
        show = Show(
            name="Seed Show",
            date=date.today() + timedelta(days=7),
            venue=venue,
            location=venue.name if venue else "",
            approved=True,
            contributor=contributor,
        )
        show.image.save("seed_show.jpg", _placeholder_image("seed_show.jpg"), save=True)
        band = Band.objects.filter(name="Local Test Band").first()
        if band:
            show.bands.add(band)
        self.stdout.write(self.style.SUCCESS("  created show: Seed Show"))
