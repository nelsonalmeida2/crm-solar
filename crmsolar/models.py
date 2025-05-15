from django.db import models
from django.db.models import IntegerField

#atribuir um criador para as classes e um utilizador atribuido e quem foi o ultimo a alterar

class Company(models.Model):
    nif = IntegerField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    segment = models.ForeignKey(Segment, on_delete=models.SET_NULL, null=True, blank=True)
    telephone = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    site = models.CharField(max_length=100, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modification_date = models.DateTimeField(auto_now=True)
    hidden = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Address(models.Model):
    address = models.CharField(max_length=240, null=True, blank=True)
    city  = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    district = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    county = models.CharField(max_length=50, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modification_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.address

class District(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    def __str__(self):
        return self.name

class Segment(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    def __str__(self):
        return self.name

class CPE(models.Model):
    cod_cpe = models.CharField(max_length=100, primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    tension = models.CharField(null=True, blank=True)
    contracted_power = models.FloatField(null=True, blank=True)
    consumption = models.FloatField(null=True, blank=True)
    provider = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    solar_panels = models.BooleanField(null=True, blank=True)
    fidelization = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=False)
    def __str__(self):
        return self.cod_cpe

class Provider(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    def __str__(self):
        return self.name

class Opportunity(models.Model):
    name = models.CharField(max_length=100)
    cpe = models.ForeignKey(CPE, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)

