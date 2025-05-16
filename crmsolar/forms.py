from django import forms
from .models import District, Country, Address, Segment, Company, Provider, CPE, OpportunityStatus, Product, Opportunity

from django import forms
from .models import Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'nif',
            'name',
            'segment',
            'phone_number',
            'email',
            'website',
            'is_hidden',
        ]
        widgets = {
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'street_address',
            'city',
            'zip_code',
            'county',
            'district',
            'country',
        ]
        widgets = {
        }
