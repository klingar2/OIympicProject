import numpy as np
import pandas as pd


file_noc = pd.read_csv('noc_regions.csv')
file_olympians_all = pd.read_csv('athlete_events.csv')
file_gdp_per_capita = pd.read_csv('GapMinder - GDP per capita - Dataset - v26 - data-for-countries-etc-by-year.csv')
file_table_gdp = pd.read_csv('total_gdp_ppp_inflation_adjusted.csv')
file_table_lifeexp = pd.read_csv('GapMinder - LifeExpectancyAtBirthTotal - Dataset.csv')

#Start & end date for analysis. Change the value of
start_date = 1948
end_date = 2012
#Olympics time Summer or Winter
olympics_type = "Summer"
# Choose Medal Type you want to examine
medal_type = "Total"

#creating a list of Olympic years using a while loop. Using start_year + 2 because the winter olympics years changed in the 1990s
olympics_years = []
start_date_x = start_date

while start_date_x < end_date:
    start_date_x = start_date_x+2
    olympics_years.append(start_date_x)
#print(olympics_years)

########################### Working with the file that contains all Olympic events (file_olympians_all)

# Subsetting file_olympians_all to only include events where the Olympian won a medal
medal = ["Gold", "Silver", "Bronze"]
only_medalists = file_olympians_all['Medal'].isin(medal)
olympians_medalists = file_olympians_all[only_medalists]
#print(file_olympians_all.shape,olympians_medalists.shape)

#filtering to only include medalists in selected type(Summer/Winter) of Olympics
#only_summer  = olympians_medalists['Season'].isin(["Summer"])
#olympians_medalists_summer = olympians_medalists[only_summer]
#print(olympians_medalists_summer.shape,olympians_medalists.shape)

only_selected  = olympians_medalists['Season'].isin([olympics_type])
olympians_medalists_selected = olympians_medalists[only_selected]
#print(olympians_medalists_selected.shape,olympians_medalists.shape)

#filter to include Olympic events 1948 onwards
modern_olympics = olympians_medalists_selected['Year'].isin(olympics_years)
olympians_medalists_selected_modern = olympians_medalists_selected[modern_olympics]
#print(olympians_medalists_selected_modern.head(3))

#Modify dataframe to add numerical columns for Gold, Silver, Bronze
olympians_medalists_selected_modern['Gold_#'] = np.where(olympians_medalists_selected_modern['Medal'] =='Gold',1,0)
olympians_medalists_selected_modern['Silver_#'] = np.where(olympians_medalists_selected_modern['Medal'] =='Silver',1,0)
olympians_medalists_selected_modern['Bronze_#'] = np.where(olympians_medalists_selected_modern['Medal'] =='Bronze',1,0)
olympians_medalists_selected_modern['Medal_#'] = np.where(olympians_medalists_selected_modern['Medal'] !='NA',1,0)
olympians_medalists_selected_modern['Medal_#'] = olympians_medalists_selected_modern['Medal_#'].astype(int)

#print(olympians_medalists_selected_modern.head(5))

# To do> Summarise medal count by Olympics games, by country
olympians_summarised = olympians_medalists_selected_modern.pivot_table(values ="Medal_#",index = ["Year","NOC","Games"], columns = "Medal",
                                                                       fill_value=0,aggfunc=np.sum)
print(olympians_summarised)


######################## working with file_table_gdp.Filter file_gdp_per_capita to include data only from 1948 onwards
gdp_per_capita_after_start_date = file_gdp_per_capita['time'].isin(olympics_years)
gdp_per_capita_modern = file_gdp_per_capita[gdp_per_capita_after_start_date]
#print(gdp_per_capita_modern.shape,file_gdp_per_capita.shape)

####################### working with file_table_gdp.
# file in table format. need to melt data based on years. found the list of year by dropping 'country'
#column names for file
gdp_table_column_names  = list(file_table_gdp.columns.values)
#dropping the name of the first column which is country
gdp_table_years = gdp_table_column_names[1:]
#print(gdp_table_years)

#gdp_table_years = gdp_table_column_names.remove("country")
#column_names_df = file_table_gdp.head(0)
#column_names_list = column_names_df.values.tolist()
file_table_gdp = file_table_gdp.fillna(0)
gdp_melted = file_table_gdp.melt(id_vars = ['country'],
                                        value_vars = gdp_table_years,
                                 var_name = ['year'], value_name = 'gdp')
gdp_melted_sorted = gdp_melted.sort_values(['country', 'year'], ascending=True)
#print(gdp_melted_sorted.head(10))

#Convert year from string to number
gdp_melted_sorted['year'] = gdp_melted_sorted['year'].astype(int)
#gdp_melted_sorted['gdp'] = gdp_melted_sorted['gdp'].astype(int)

# need to remove irrelevant years. I know I don't need to this. As I can just join this dataframe to summarized Olympic table. Doing this step for practicing subsetting dataframes
gdp_melted_sorted_olympic_years = gdp_melted_sorted['year'].isin(olympics_years)
gdp_melted_sorted_relevant = gdp_melted_sorted[gdp_melted_sorted_olympic_years]
#print(gdp_melted_sorted_relevant.head())

####################### working with the file_table_lifeexp
#column names for file
lifeexp_table_column_names  = list(file_table_lifeexp.columns.values)
#dropping the name of the first column which is country
lifeexp_table_years = lifeexp_table_column_names[1:]
#print(lifeexp_table_years)

file_table_lifeexp = file_table_lifeexp.fillna(0)
lifeexp_melted = file_table_lifeexp.melt(id_vars = ['country'],
                                        value_vars = lifeexp_table_years,
                                 var_name = ['year'], value_name = 'life_expectancy')
lifeexp_melted_sorted = lifeexp_melted.sort_values(['country', 'year'], ascending=True)
#print(lifeexp_melted_sorted.head(10))


#Using Numpy https://stackabuse.com/calculating-pearson-correlation-coefficient-in-python-with-numpy/ to tell the corellation between GDP and olmypic performance
