# clients/models.py

from django.db import models
from core.models import TimeStampedUserModel, Address, Segment, BuildingType  # Importa do core


class CompanyGroup(TimeStampedUserModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    segment = models.ForeignKey(
        Segment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='groups'
    )
    # M2M com Contact (na mesma app)
    contacts = models.ManyToManyField(
        'Contact',
        blank=True,
        related_name='groups'
    )

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


class Company(TimeStampedUserModel):
    # O seu modelo original usava IntegerField para NIF (que é a PK).
    # NIF é uma chave única, geralmente tratada como String/CharField para evitar problemas com zeros à esquerda.
    nif = models.CharField(max_length=20, primary_key=True, verbose_name="NIF")
    name = models.CharField(max_length=100)

    # Relações com o módulo CORE
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    segment = models.ForeignKey(Segment, on_delete=models.SET_NULL, null=True, blank=True)
    type_of_building = models.ForeignKey(BuildingType, on_delete=models.SET_NULL, null=True, blank=True)

    # Relações dentro desta APP
    group = models.ForeignKey(
        CompanyGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='companies'
    )
    contacts = models.ManyToManyField(
        Contact,
        blank=True,
        related_name='companies'
    )

    # Campos próprios
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    has_solar_panels = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name