import numpy as np
import pandas as pd


file_noc = pd.read_csv('noc_regions.csv')
file_olympians_all = pd.read_csv('athlete_events.csv')
file_gdp_per_capita = pd.read_csv('GapMinder - GDP per capita - Dataset - v26 - data-for-countries-etc-by-year.csv')
file_table_gdp = pd.read_csv('total_gdp_ppp_inflation_adjusted.csv')
file_table_lifeexp = pd.read_csv('GapMinder - LifeExpectancyAtBirthTotal - Dataset.csv')


# Working with the file that contains all Olympic events

# Subsetting file_olympians_all to only include events where the Olympian won a medal
medal = ["Gold", "Silver", "Bronze"]
only_medalists = file_olympians_all['Medal'].isin(medal)
olympians_medalists = file_olympians_all[only_medalists]
#print(file_olympians_all.shape,olympians_medalists.shape)

#filtering to only include medalists in summer Olympics
only_summer  = olympians_medalists['Season'].isin(["Summer"])
olympians_medalists_summer = olympians_medalists[only_summer]
#print(olympians_medalists_summer.shape,olympians_medalists.shape)

#filter to include Olympic events 1948 onwards
modern_olympics = olympians_medalists_summer['Year']>=1948
olmypians_medalists_summer_modern = olympians_medalists_summer[modern_olympics]
#print(olmypians_medalists_summer_modern.shape)



