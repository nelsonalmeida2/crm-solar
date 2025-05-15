from django.db import models
from django.db.models import IntegerField


# Create your models here.

class Company(models.Model):
    nif = IntegerField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=240, null=True, blank=True)
    city  = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    county = models.CharField(max_length=50, null=True, blank=True)
    telephone = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    site = models.CharField(max_length=100, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modification_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name



