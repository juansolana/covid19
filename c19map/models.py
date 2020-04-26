from django.contrib.gis.db import models
from django.contrib.auth.models import  User
from django.db.models.signals import post_save
from django.dispatch import receiver
# from mapbox_location_field.spatial.models import SpatialLocationField

# Create your models here.
class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    curp = models.CharField(max_length=18, default="XXXX000000XXXXXX00")
    location = models.PointField()
    # location = SpatialLocationField()
    latitude = models.FloatField(default=23.0)
    longitude = models.FloatField(default=-102.0)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=5)
    verified = models.BooleanField(default=False)
    email = models.EmailField(default='a@example.com')
    temperature = models.FloatField(default=36.5)
    age = models.IntegerField(default=18)
    sex = models.TextField(default='')
    tos = models.BooleanField(default=False)
    cabeza = models.BooleanField(default=False)
    garganta = models.BooleanField(default=False)
    respiracion = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_person_signal(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance)
    instance.person.save()
