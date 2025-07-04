from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    District,
    Country,
    Address,
    Segment,
    BuildingType,
    Company,
    Provider,
    CPE,
    OpportunityStatus,
    Product,
    Opportunity,
    CalendarEntry,
    Priority,
    TaskType,
    Task
)

# Modelos SEM histórico
admin.site.register(District)
admin.site.register(Country)
admin.site.register(Segment)
admin.site.register(BuildingType)
admin.site.register(Provider)
admin.site.register(OpportunityStatus)
admin.site.register(Product)
admin.site.register(CalendarEntry)
admin.site.register(Priority)
admin.site.register(TaskType)

# Modelos COM histórico
admin.site.register(Address, SimpleHistoryAdmin)
admin.site.register(Company, SimpleHistoryAdmin)
admin.site.register(CPE, SimpleHistoryAdmin)
admin.site.register(Opportunity, SimpleHistoryAdmin)
admin.site.register(Task, SimpleHistoryAdmin)
