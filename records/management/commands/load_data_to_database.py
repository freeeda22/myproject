# load_production_data.py
from django.core.management.base import BaseCommand
import pandas as pd
from records.models import ProductionData, WellNumber

class Command(BaseCommand):
    help = 'Loads production data from an Excel file into the database'

    def handle(self, *args, **kwargs):
        file_path = 'records/excel_data/production_data.xls'
        df = pd.read_excel(file_path)

        # Iterate through DataFrame and save to DB
        for index, row in df.iterrows():
            well_obj, created = WellNumber.objects.get_or_create(well_number=row['API WELL  NUMBER'])
            print(well_obj)
            obj = ProductionData.objects.filter(api_well_number=well_obj,
                                                year=row['Production Year'],
                                                quarter=row['QUARTER 1,2,3,4']
                                                ).exists()
            if obj:
                continue
            else:
                production_data = ProductionData(
                    api_well_number=well_obj,
                    year=row['Production Year'],
                    quarter=row['QUARTER 1,2,3,4'],
                    owner_name=row['OWNER NAME'],
                    country=row['COUNTY'],
                    township=row['TOWNSHIP'],
                    well_name=row['WELL NAME'],
                    well_number=row['WELL NUMBER'],
                    oil_production=row['OIL'],
                    gas_production=row['GAS'],
                    brine_production=row['BRINE'],
                    days=row['DAYS'],
                )
                production_data.save()

        return 'Data loaded successfully!'
