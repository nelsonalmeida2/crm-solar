# core/models.py

from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords


# ======================================================================
# 1. ABSTRACT BASE MODEL
# ======================================================================

class TimeStampedUserModel(models.Model):
    """
    Abstract base class providing common fields (timestamps, audit trail, assignment).
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created"
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated"
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_assigned"
    )

    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True


# ======================================================================
# 2. REFERENCE / GLOBAL MODELS (Data/Geography/Types)
# ======================================================================

class District(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    districts = models.ManyToManyField(District, related_name='countries')

    def __str__(self):
        return self.name


class Address(TimeStampedUserModel):
    id = models.AutoField(primary_key=True)
    street_address = models.CharField(max_length=240, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    county = models.CharField(max_length=50, null=True, blank=True)  # County/Parish

    def __str__(self):
        return self.street_address or f"Address ID: {self.id}"


class Segment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)  # E.g., Residential, Industrial, Retail

    def __str__(self):
        return self.name


class BuildingType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)  # E.g., Single-family house, Warehouse, Office

    def __str__(self):
        return self.name


class Provider(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)  # E.g., EDP, Endesa, Goldenergy

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)  # E.g., Residential Solar, Gas Supply, Energy Audit
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class CalendarEntry(models.Model):
    """ Used for reporting/BI purposes """
    id = models.AutoField(primary_key=True)
    date = models.DateField(unique=True)
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


# ======================================================================
# 3. GLOBAL ENTITIES (TASK & TASK TYPE)
# ======================================================================

class TaskType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)  # E.g., Call, Meeting, Email

    def __str__(self):
        return self.name


class Task(TimeStampedUserModel):
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    start_datetime = models.DateTimeField()
    due_datetime = models.DateTimeField()
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.SET_NULL, null=True)
    completed = models.BooleanField(default=False)

    # RELATIONS TO OTHER APPS (Using lazy string references)
    opportunity = models.ForeignKey(
        'sales.Opportunity',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )
    company = models.ForeignKey(
        'clients.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )
    contact = models.ForeignKey(
        'clients.Contact',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )

    def __str__(self):
        return self.title


# ======================================================================
# 4. TRANSVERSAL ENTITIES (OBSERVATION)
# ======================================================================

class Observation(TimeStampedUserModel):
    """ Flexible model to attach notes/observations to multiple entities """
    id = models.AutoField(primary_key=True)
    text = models.TextField()

    # Internal reference to Task (now in core)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True, related_name='observations')

    # Relations to other apps (string quotes needed):
    cpe = models.ForeignKey('energy.CPE', on_delete=models.CASCADE, null=True, blank=True, related_name='observations')
    company = models.ForeignKey('clients.Company', on_delete=models.CASCADE, null=True, blank=True,
                                related_name='observations')
    opportunity = models.ForeignKey('sales.Opportunity', on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='observations')
    contact = models.ForeignKey('clients.Contact', on_delete=models.CASCADE, null=True, blank=True,
                                related_name='observations')
    group = models.ForeignKey('clients.CompanyGroup', on_delete=models.CASCADE, null=True, blank=True,
                              related_name='observations')

    def __str__(self):
        return self.text[:50]