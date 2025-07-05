from datetime import date, timedelta
from crmsolar.models import CalendarEntry

start_date = date(2020, 1, 1)
end_date = date(2030, 12, 31)

current_date = start_date
entries = []

while current_date <= end_date:
    entry = CalendarEntry(
        date=current_date,
        day=current_date.day,
        month=current_date.month,
        year=current_date.year,
        quarter=((current_date.month - 1) // 3) + 1
    )
    entries.append(entry)
    current_date += timedelta(days=1)

CalendarEntry.objects.bulk_create(entries)

print(f"Inserted {len(entries)} calendar entries from {start_date} to {end_date}.")
