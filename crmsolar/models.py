from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords

class District(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    districts = models.ManyToManyField(District)

    def __str__(self):
        return self.name

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    street_address = models.CharField(max_length=240, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    county = models.CharField(max_length=50, null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.street_address or "Address"

class Segment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class BuildingType(models.Model):  # antigo Type_of_Building
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Company(models.Model):
    nif = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='companies_assigned')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    segment = models.ForeignKey(Segment, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    has_solar_panels = models.BooleanField(default=False)
    type_of_building = models.ForeignKey(BuildingType, on_delete=models.SET_NULL, null=True, blank=True)
    is_hidden = models.BooleanField(default=False)

    history = HistoricalRecords()

    def __str__(self):
        return self.name

class Provider(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class CPE(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100, unique=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='cpes_assigned')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    tension = models.CharField(max_length=50, null=True, blank=True)
    contracted_power = models.FloatField(null=True, blank=True)
    consumption = models.FloatField(null=True, blank=True)
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True, blank=True)
    has_solar_panels = models.BooleanField(default=False)
    type_of_building = models.ForeignKey(BuildingType, on_delete=models.SET_NULL, null=True, blank=True)
    fidelization_end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    history = HistoricalRecords()

    def __str__(self):
        return self.code

class OpportunityStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Opportunity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='opportunities_assigned')
    cpe = models.ForeignKey(CPE, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    opportunity_status = models.ForeignKey(OpportunityStatus, on_delete=models.SET_NULL, null=True)
    opportunity_value = models.FloatField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    exclusivity_expires_at = models.DateTimeField()

    history = HistoricalRecords()

    def __str__(self):
        return self.name

class CalendarEntry(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    day = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    quarter = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()

    def save(self, *args, **kwargs):
        self.day = self.date.day
        self.month = self.date.month
        self.year = self.date.year
        self.quarter = ((self.month - 1) // 3) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.date.strftime("%d/%m/%Y")


class Priority(models.Model):
    name = models.CharField(max_length=50, unique=True)
    level = models.PositiveIntegerField(help_text="Nível de prioridade, por exemplo 1 para alta, 2 para média, etc.")

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    start_datetime = models.DateTimeField()
    due_datetime = models.DateTimeField()
    reminder_datetime = models.DateTimeField(null=True, blank=True)

    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True)
    task_type = models.ForeignKey(TaskType, on_delete=models.SET_NULL, null=True)

    completed = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.title
