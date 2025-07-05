from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords


class TimeStampedUserModel(models.Model):
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


class Address(TimeStampedUserModel):
    id = models.AutoField(primary_key=True)
    street_address = models.CharField(max_length=240, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    county = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.street_address or "Address"


class Segment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class BuildingType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Observation(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    cpe = models.ForeignKey('CPE', on_delete=models.CASCADE, null=True, blank=True, related_name='observations')
    task = models.ForeignKey('Task', on_delete=models.CASCADE, null=True, blank=True, related_name='observations')
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True, related_name='observations')
    opportunity = models.ForeignKey('Opportunity', on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='observations')
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE, null=True, blank=True, related_name='observations')
    group = models.ForeignKey('CompanyGroup', on_delete=models.CASCADE, null=True, blank=True,
                              related_name='observations')

    def __str__(self):
        return self.text[:50]


class Company(TimeStampedUserModel):
    nif = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    segment = models.ForeignKey(Segment, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    has_solar_panels = models.BooleanField(default=False)
    type_of_building = models.ForeignKey(BuildingType, on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(
        'CompanyGroup',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='companies'
    )
    contacts = models.ManyToManyField(
        'Contact',
        blank=True,
        related_name='companies'
    )
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Contact(TimeStampedUserModel):
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=100)
    department = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    PREFERRED_METHOD_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('mobile', 'Mobile'),
    ]
    preferred_contact_method = models.CharField(
        max_length=10,
        choices=PREFERRED_METHOD_CHOICES,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class CompanyGroup(TimeStampedUserModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    segment = models.ForeignKey(
        'Segment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='groups'
    )
    contacts = models.ManyToManyField(
        'Contact',
        blank=True,
        related_name='groups'
    )

    def __str__(self):
        return self.name


class Provider(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class CPE(TimeStampedUserModel):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100, unique=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    tension = models.CharField(max_length=50, null=True, blank=True)
    contracted_power = models.FloatField(null=True, blank=True)
    consumption = models.FloatField(null=True, blank=True)
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True, blank=True)
    has_solar_panels = models.BooleanField(default=False)
    type_of_building = models.ForeignKey(BuildingType, on_delete=models.SET_NULL, null=True, blank=True)
    fidelization_end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

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


class Opportunity(TimeStampedUserModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    cpe = models.ForeignKey(CPE, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    opportunity_status = models.ForeignKey(OpportunityStatus, on_delete=models.SET_NULL, null=True)
    opportunity_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Estimated value of the opportunity"
    )
    revenue = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Actual revenue if the opportunity is closed"
    )
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    exclusivity_expires_at = models.DateTimeField()

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


class TaskType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

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

    def __str__(self):
        return self.title
