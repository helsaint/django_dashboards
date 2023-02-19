from django.db import models

class Regions(models.Model):
    country = models.TextField(blank=True, null=True)
    continent = models.TextField(blank=True, null=True)
    sub_region = models.TextField(blank=True,null=True)

    class Meta:
        managed = False
        db_table = 'countries_region'

class Countries(models.Model):
    index = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    alpha_2 = models.TextField(db_column='Alpha_2', blank=True, null=True)  # Field name made lowercase.
    alpha_3 = models.TextField(db_column='Alpha_3', blank=True, null=True)  # Field name made lowercase.
    numeric_code = models.TextField(blank=True, null=True)
    latitude_average = models.TextField(blank=True, null=True)
    longitude_average = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blackDB_countries'


class Emissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    index = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    year = models.TextField(blank=True, null=True)
    iso_code = models.TextField(blank=True, null=True)
    population = models.TextField(blank=True, null=True)
    gdp = models.TextField(blank=True, null=True)
    cement_co2 = models.TextField(blank=True, null=True)
    cement_co2_per_capita = models.TextField(blank=True, null=True)
    co2 = models.TextField(blank=True, null=True)
    co2_growth_abs = models.TextField(blank=True, null=True)
    co2_growth_prct = models.TextField(blank=True, null=True)
    co2_per_capita = models.TextField(blank=True, null=True)
    co2_per_gdp = models.TextField(blank=True, null=True)
    co2_per_unit_energy = models.TextField(blank=True, null=True)
    coal_co2 = models.TextField(blank=True, null=True)
    coal_co2_per_capita = models.TextField(blank=True, null=True)
    consumption_co2 = models.TextField(blank=True, null=True)
    consumption_co2_per_capita = models.TextField(blank=True, null=True)
    consumption_co2_per_gdp = models.TextField(blank=True, null=True)
    cumulative_cement_co2 = models.TextField(blank=True, null=True)
    cumulative_co2 = models.TextField(blank=True, null=True)
    cumulative_coal_co2 = models.TextField(blank=True, null=True)
    cumulative_flaring_co2 = models.TextField(blank=True, null=True)
    cumulative_gas_co2 = models.TextField(blank=True, null=True)
    cumulative_oil_co2 = models.TextField(blank=True, null=True)
    cumulative_other_co2 = models.TextField(blank=True, null=True)
    energy_per_capita = models.TextField(blank=True, null=True)
    energy_per_gdp = models.TextField(blank=True, null=True)
    flaring_co2 = models.TextField(blank=True, null=True)
    flaring_co2_per_capita = models.TextField(blank=True, null=True)
    gas_co2 = models.TextField(blank=True, null=True)
    gas_co2_per_capita = models.TextField(blank=True, null=True)
    ghg_excluding_lucf_per_capita = models.TextField(blank=True, null=True)
    ghg_per_capita = models.TextField(blank=True, null=True)
    methane = models.TextField(blank=True, null=True)
    methane_per_capita = models.TextField(blank=True, null=True)
    nitrous_oxide = models.TextField(blank=True, null=True)
    nitrous_oxide_per_capita = models.TextField(blank=True, null=True)
    oil_co2 = models.TextField(blank=True, null=True)
    oil_co2_per_capita = models.TextField(blank=True, null=True)
    other_co2_per_capita = models.TextField(blank=True, null=True)
    other_industry_co2 = models.TextField(blank=True, null=True)
    primary_energy_consumption = models.TextField(blank=True, null=True)
    share_global_cement_co2 = models.TextField(blank=True, null=True)
    share_global_co2 = models.TextField(blank=True, null=True)
    share_global_coal_co2 = models.TextField(blank=True, null=True)
    share_global_cumulative_cement_co2 = models.TextField(blank=True, null=True)
    share_global_cumulative_co2 = models.TextField(blank=True, null=True)
    share_global_cumulative_coal_co2 = models.TextField(blank=True, null=True)
    share_global_cumulative_flaring_co2 = models.TextField(blank=True, null=True)
    share_global_cumulative_gas_co2 = models.TextField(blank=True, null=True)
    share_global_cumulative_oil_co2 = models.TextField(blank=True, null=True)
    share_global_cumulative_other_co2 = models.TextField(blank=True, null=True)
    share_global_flaring_co2 = models.TextField(blank=True, null=True)
    share_global_gas_co2 = models.TextField(blank=True, null=True)
    share_global_oil_co2 = models.TextField(blank=True, null=True)
    share_global_other_co2 = models.TextField(blank=True, null=True)
    total_ghg = models.TextField(blank=True, null=True)
    total_ghg_excluding_lucf = models.TextField(blank=True, null=True)
    trade_co2 = models.TextField(blank=True, null=True)
    trade_co2_share = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blackDB_emissions'


# Create your models here.

