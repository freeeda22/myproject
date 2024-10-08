# Generated by Django 5.1.1 on 2024-10-08 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductionData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_well_number', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('quarter', models.IntegerField()),
                ('owner_name', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('township', models.CharField(max_length=100)),
                ('well_name', models.CharField(max_length=100)),
                ('well_number', models.CharField(max_length=100)),
                ('oil_production', models.IntegerField()),
                ('gas_production', models.IntegerField()),
                ('brine_production', models.IntegerField()),
                ('days', models.IntegerField()),
            ],
        ),
    ]
