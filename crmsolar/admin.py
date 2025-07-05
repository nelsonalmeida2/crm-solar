from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    District,
    Country,
    Address,
    Segment,
    BuildingType,
    Observation,
    Contact,
    Company,
    CompanyGroup,
    Provider,
    CPE,
    OpportunityStatus,
    Product,
    Opportunity,
    CalendarEntry,
    TaskType,
    Task,
)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    filter_horizontal = ('districts',)


@admin.register(Address)
class AddressAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'street_address', 'city', 'zip_code', 'district', 'country')
    search_fields = ('street_address', 'city', 'zip_code')
    list_filter = ('country', 'district')


@admin.register(Segment)
class SegmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(BuildingType)
class BuildingTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'task',
        'company',
        'group',
        'contact',
        'opportunity',
        'cpe',
    )
    search_fields = ('text',)
    list_filter = ('task', 'company', 'group', 'contact', 'opportunity', 'cpe')


class ContactAdmin(SimpleHistoryAdmin):
    list_display = (
        'id',
        'name',
        'company_group',
        'role',
        'phone',
        'email',
        'preferred_contact_method',
        'is_primary',
        'is_active',
    )
    search_fields = ('name', 'email', 'phone')
    list_filter = (
        'is_primary',
        'is_active',
        'preferred_contact_method',
        'company_group',
    )


@admin.register(Company)
class CompanyAdmin(SimpleHistoryAdmin):
    list_display = ('nif', 'name', 'segment', 'phone_number', 'email', 'website', 'has_solar_panels', 'is_hidden')
    search_fields = ('name', 'nif', 'email')
    list_filter = ('segment', 'has_solar_panels', 'is_hidden')


@admin.register(CompanyGroup)
class CompanyGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'segment')
    search_fields = ('name',)
    list_filter = ('segment',)


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(CPE)
class CPEAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'code', 'company', 'provider', 'contracted_power', 'consumption', 'has_solar_panels',
                    'is_active')
    search_fields = ('code',)
    list_filter = ('provider', 'has_solar_panels', 'is_active')


@admin.register(OpportunityStatus)
class OpportunityStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Opportunity)
class OpportunityAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'name', 'company', 'cpe', 'opportunity_status', 'opportunity_value', 'revenue', 'product',
                    'closed_at')
    search_fields = ('name',)
    list_filter = ('opportunity_status', 'product', 'closed_at')


@admin.register(CalendarEntry)
class CalendarEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'day', 'month', 'quarter', 'year')
    list_filter = ('year', 'quarter', 'month')


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'title', 'priority', 'start_datetime', 'due_datetime', 'completed')
    list_filter = ('priority', 'completed', 'task_type')
    search_fields = ('title', 'description')
