import numpy as np
import pandas as pd


file_noc = pd.read_csv('noc_regions.csv')
file_olympics = pd.read_csv('athlete_events.csv')
file_gdp_per_capita = pd.read_csv('GapMinder - GDP per capita - Dataset - v26 - data-for-countries-etc-by-year.csv')
file_table_gdp = pd.read_csv('total_gdp_ppp_inflation_adjusted.csv')
file_table_lifeexp = pd.read_csv('GapMinder - LifeExpectancyAtBirthTotal - Dataset.csv')

print(file_gdp_per_capita.head(6))