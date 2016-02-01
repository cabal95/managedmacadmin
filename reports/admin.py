from django.contrib import admin
from reports.models import Machine, Fact, HistoricalFact

admin.site.register(Machine)
admin.site.register(Fact)
admin.site.register(HistoricalFact)
