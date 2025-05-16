from django.db import models
from django.conf import settings

#TODO CRIAR TAREFAS E CALENDARIO

class District(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name

class Address(models.Model):
    street_address = models.CharField(max_length=240, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    county = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.street_address or "Address"

class Segment(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name

class Company(models.Model):
    nif = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='companies_created')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='companies_assigned')
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='companies_modified')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    segment = models.ForeignKey(Segment, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Provider(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name

class CPE(models.Model):
    code = models.CharField(max_length=100, primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='cpes_created')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='cpes_assigned')
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='cpes_modified')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    tension = models.CharField(max_length=50, null=True, blank=True)
    contracted_power = models.FloatField(null=True, blank=True)
    consumption = models.FloatField(null=True, blank=True)
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True, blank=True)
    has_solar_panels = models.BooleanField(null=True, blank=True)
    fidelization_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.code

class OpportunityStatus(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Opportunity(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='opportunities_created')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='opportunities_assigned')
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='opportunities_modified')
    cpe = models.ForeignKey(CPE, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    opportunity_status = models.ForeignKey(OpportunityStatus, on_delete=models.SET_NULL)
    opportunity_value = models.FloatField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    exclusivity_expires_at = models.DateTimeField()

    def __str__(self):
        return self.name
