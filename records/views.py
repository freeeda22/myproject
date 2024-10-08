# records/views.py

import pandas as pd
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.conf import settings
import os
from .models import ProductionData, AnnualData , WellNumber
from .serializers import ProductionDataSerializer

class DownloadFilteredProductionData(APIView):
    """
    to download filtered production data from an Excel file.
    Users can filter by year and/or quarter via query parameters.
    """

    def get(self, request):
        # Extract filters from the request
        year = request.GET.get('year')
        quarter = request.GET.get('quarter')

        # Construct the path to the Excel file
        file_path = os.path.join(settings.BASE_DIR, 'records', 'excel_data', 'production_data.xls')

        # Attempt to read and filter the Excel data
        try:
            df = pd.read_excel(file_path)

            # Apply filters if provided
            if year:
                df = df[df['Production Year'] == int(year)]
            if quarter:
                df = df[df['QUARTER 1,2,3,4'] == int(quarter)]

            # Check if the filtered DataFrame is empty
            if df.empty:
                return HttpResponse("No data found for the specified filters.", status=404)

            # Prepare the response with the filtered data
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="filtered_production_data.xlsx"'

            with pd.ExcelWriter(response, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)

            return response

        except Exception as e:
            return HttpResponse(f'Error reading the file: {e}', status=500)

class  ProductionAnnualData(APIView):
    """
    calculate annual  data of a well number
    """
    def get(self, request):
        try:
            well_number = request.GET.get('well_number')
            instance = ProductionData.objects.filter(api_well_number__well_number=well_number)
            oil_data = sum(instance.values_list('oil_production', flat=True))
            gas_data = sum(instance.values_list('gas_production', flat=True))
            brine_data = sum(instance.values_list('brine_production', flat=True))
            obj_exists = WellNumber.objects.filter(well_number = well_number).exists()
            if obj_exists:
                annual_obj = AnnualData.objects.filter(well_number__well_number = well_number).exists()
                if annual_obj:
                    obj =  AnnualData.objects.get(well_number__well_number = well_number)
                    obj.annual_oil_production = oil_data
                    obj.annual_gas_production = gas_data
                    obj.annual_brine_production = brine_data
                    obj.save()
                else:
                    well_obj = WellNumber.objects.get(well_number = well_number)
                    AnnualData.objects.create(well_number = well_obj, annual_oil_production=oil_data,
                                          annual_gas_production = gas_data, annual_brine_production = brine_data )
            else:
                well_obj = WellNumber.objects.create(well_number = well_number)
                AnnualData.objects.create(well_number = well_obj, annual_oil_production=oil_data,
                                          annual_gas_production = gas_data, annual_brine_production = brine_data )
            data = {
                "oil" : oil_data,
                "gas" : gas_data,
                "brine" : brine_data,
            }
            return Response(data)
        except ProductionData.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

class DeleteAllRecordsView(APIView):
    """
    delete all records
    """
    def delete(self, request, *args, **kwargs):
        try:
            # Delete all records
            ProductionData.objects.all().delete()
            return Response({"message": "All records deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

class  ProductionDataWellNumber(APIView):
    """
    return data of a particular wel data
    """
    def get(self, request):
        try:
            well_number = request.GET.get('well_number')
            instance = ProductionData.objects.filter(api_well_number__well_number=well_number)
            if not well_number:
                return Response({"error": "well_number is required"})
            if instance.exists():
                serializer = ProductionDataSerializer(instance, many=True)
                return Response(serializer.data, status=200)
            else:
                return Response({"message": "No production data found for this well number"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
