# models.py
from django.db import models

class WellNumber(models.Model):
    id = models.AutoField(primary_key=True)
    well_number = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return f"Well {self.well_number}"

class ProductionData(models.Model):
    id = models.AutoField(primary_key=True)
    api_well_number = models.ForeignKey(WellNumber, on_delete=models.CASCADE)
    year = models.IntegerField()
    quarter = models.IntegerField()
    owner_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    township = models.CharField(max_length=100)
    well_name = models.CharField(max_length=100)
    well_number = models.CharField(max_length=100)
    oil_production = models.IntegerField()
    gas_production = models.IntegerField()
    brine_production = models.IntegerField()
    days = models.IntegerField()

    def __str__(self):
        return f"Well {self.api_well_number} - Year {self.year} Q{self.quarter}"

class AnnualData(models.Model):
    id = models.AutoField(primary_key=True)
    well_number = models.ForeignKey(WellNumber, on_delete=models.CASCADE)
    annual_oil_production = models.IntegerField()
    annual_gas_production = models.IntegerField()
    annual_brine_production = models.IntegerField()

    def __str__(self):
        return f"Well {self.well_number.well_number}"
