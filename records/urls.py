from django.urls import path
from .views import ( DownloadFilteredProductionData, 
                    ProductionAnnualData,DeleteAllRecordsView,
                    ProductionDataWellNumber)

urlpatterns = [
    path('export_data/', DownloadFilteredProductionData.as_view(), name='export'), 
    path('annual_data/', ProductionAnnualData.as_view(), name="annual_data") ,
    path('delete/', DeleteAllRecordsView.as_view()),
    path('well_detail/', ProductionDataWellNumber.as_view())
]