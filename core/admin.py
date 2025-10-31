# core/admin.py

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    District, Country, Address, Segment, BuildingType, Provider, Product,
    CalendarEntry, Observation, TaskType, Task # TimeStampedUserModel is abstract, not registered
)

# ----------------------------------------------------------------------
# ADMIN CLASSES
# ----------------------------------------------------------------------

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
    list_display = ('id', 'street_address', 'city', 'zip_code', 'district', 'country', 'county')
    search_fields = ('street_address', 'city', 'zip_code')
    list_filter = ('country', 'district')
    raw_id_fields = ('district', 'country')


@admin.register(Segment)
class SegmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(BuildingType)
class BuildingTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


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
    list_filter = ('priority', 'completed', 'task_type', 'created_at') # 'created_at' is now safe
    search_fields = ('title', 'description')
    raw_id_fields = ('task_type', 'opportunity', 'company', 'contact')


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'text', 'task', 'company', 'group', 'contact', 'opportunity', 'cpe', 'created_at', 'updated_at'
    )
    search_fields = ('text',)
    # list_filter now works because created_at/updated_at exist
    list_filter = ('created_at', 'updated_at')
    raw_id_fields = ('task', 'company', 'group', 'contact', 'opportunity', 'cpe')