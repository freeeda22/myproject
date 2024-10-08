from django.contrib import admin
from.models import ProductionData, WellNumber, AnnualData
# Register your models here.

admin.site.register(ProductionData)
admin.site.register(WellNumber)
admin.site.register(AnnualData)