from django.conf import settings
from django.db import models
# Create your models here.


class Location(models.Model):
    Country = models.CharField( max_length=50) 

    def __str__(self):
        return self.Country