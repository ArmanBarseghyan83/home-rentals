from django.contrib.auth.models import AbstractUser
from django.db import models

import geocoder

token = 'pk.eyJ1IjoiYXJtYW5iYXJzZWdoeWFuIiwiYSI6ImNsOXJzZmJzZTBqYjIzd21kbDQ0anExb24ifQ.bIuDExySY92cE1D3CzcWdw'

class User(AbstractUser):
    pass


class Property(models.Model):
    home_type_name = models.CharField(max_length=100)

    def __str__(self):
        return self.home_type_name


class Listing(models.Model):
    home_type = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True, related_name="listings")
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=100)
    lot = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    price = models.FloatField(max_length=100, null=True, blank=True)
    bed = models.IntegerField(null=True, blank=True)
    bath = models.IntegerField(null=True, blank=True)
    year_built = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings" )
    saved = models.ManyToManyField(User, blank=True, related_name="saved")
    
    def save(self, *args, **kwargs):
        try:
            g = geocoder.mapbox(self.address, key=token)
            g = g.latlng # [lat, long]
            self.lot = g[0]
            self.long = g[1]
            return super(Listing, self).save(*args, **kwargs)
        except:
            return super(Listing, self).save(*args, **kwargs)

    def __str__(self):
        return self.address
    
class TourRequest(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="tour_requests")
    sender = models.ForeignKey("User", on_delete=models.PROTECT, related_name="sent")
    recipients = models.ManyToManyField("User", related_name="mailbox")
    subject = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender}: {self.listing}"
       
