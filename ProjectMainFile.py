import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 20)
pd.options.display.float_format = '{:.0f}'.format

#================================ IMPORTING THE FILES TO BE USED

file_noc = pd.read_csv('noc_regions.csv')
file_olympians_all = pd.read_csv('athlete_events.csv')
file_gdp_per_capita = pd.read_csv('GapMinder - GDP per capita - Dataset - v26 - data-for-countries-etc-by-year.csv')
file_table_gdp = pd.read_csv('total_gdp_ppp_inflation_adjusted.csv')
file_table_lifeexp = pd.read_csv('GapMinder - LifeExpectancyAtBirthTotal - Dataset.csv')
file_noc_iso = pd.read_csv('NOC_ISO_FIFA.csv')
#print(file_noc_iso.head())

#============================= PARAMETERS THAT CAN BE ADJUSTED FOR ANALYSIS
#################### Choose the type of analysis you would like to do
#Start & end date for analysis. Specify the range of Olympics,
start_date = 1948
end_date = 2012
#Olympics time Summer or Winter
olympics_type = "Summer"
# Choose Medal Type you want to examine [Total/Gold/Silver/Bronze]
medal_type_analysis = 'Total'

#creating a list of Olympic years using a while loop. Using start_year + 2 because the winter olympics years changed in the 1990s
olympics_years = []
start_date_x = start_date

while start_date_x < end_date:
    start_date_x = start_date_x+2
    olympics_years.append(start_date_x)
#print(olympics_years)

#==========================IMPORTING FILES AND TRANSFORMING THEM (WITHOUT ANY MERGES)
########################### Working with the file that contains all Olympic events (file_olympians_all)

# Subsetting file_olympians_all to only include events where the Olympian won a medal
file_olympians_all['Gold_#'] = np.where(file_olympians_all['Medal'] =='Gold',1,0)
file_olympians_all['Silver_#'] = np.where(file_olympians_all['Medal'] =='Silver',1,0)
file_olympians_all['Bronze_#'] = np.where(file_olympians_all['Medal'] =='Bronze',1,0)
file_olympians_all['Medal_#'] = np.where(file_olympians_all['Medal'] !='NA',1,0)

# changing medal to conditional variable what is chosen by user
#medal = ["Gold", "Silver", "Bronze"]
if "Total" == medal_type_analysis:
    medal = ["Gold", "Silver", "Bronze"]
elif "Gold" == medal_type_analysis:
    medal = ["Gold"]
elif "Silver" == medal_type_analysis:
    medal =["Silver"]
elif "Bronze" == medal_type_analysis:
    medal = ["Bronze"]

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

#Modify dataframe to add numerical columns for Gold, Silver, Bronze. **** this is creating a 'SettingWithCopyWarning' ERROR so added columns at
#olympians_medalists_selected_modern['Gold_#'] = np.where(olympians_medalists_selected_modern['Medal'] =='Gold',1,0)
#olympians_medalists_selected_modern['Silver_#'] = np.where(olympians_medalists_selected_modern['Medal'] =='Silver',1,0)
#olympians_medalists_selected_modern['Bronze_#'] = np.where(olympians_medalists_selected_modern['Medal'] =='Bronze',1,0)
#olympians_medalists_selected_modern['Medal_#'] = np.where(olympians_medalists_selected_modern['Medal'] !='NA',1,0)
#olympians_medalists_selected_modern['Medal_#'] = olympians_medalists_selected_modern['Medal_#'].astype(int)

#print(olympians_medalists_selected_modern.head(5))

###################### MERGING olympians_medalists_selected_modern that contains NOC codes with NOC_IOC that contains NOC and ISO3 codes (since other datasets use ISO3 code)

olympians_medalists_selected_modern = olympians_medalists_selected_modern.merge(file_noc_iso, how = 'left',
                                                             left_on = 'NOC', right_on = 'IOC',
                                                             suffixes = ('_OLY','_GPC'))

#print(olympians_medalists_selected_modern.head(25))

# To do> Summarise medal count by Olympics games, by country.
olympians_summarised = olympians_medalists_selected_modern.pivot_table(values ="Medal_#",
                                                                       index = ["Year","Team" ,"ISO","NOC", "Games"],
                                                                       columns = "Medal",
                                                                       margins = True,
                                                                       fill_value=0,
                                                                      aggfunc=np.sum)

#print(olympians_summarised.head(25))

#print(olympians_summarised.head(1))
#olympians_summarised.to_csv(r'C:\Users\Kiran\Google Drive\Learning\03 - UCD - intro to Python\10. Final Project\Data\CSVs from Pandas\olympians_summarised.csv', index = False, header = True)

######################## working with file_gdp_per_capita. Filter file_gdp_per_capita to inlclude only years in range
file_gdp_per_capita['geo'] = file_gdp_per_capita['geo'].str.upper()
gdp_per_capita_after_start_date = file_gdp_per_capita['time'].isin(olympics_years)
gdp_per_capita_modern = file_gdp_per_capita[gdp_per_capita_after_start_date]
#print(gdp_per_capita_modern.shape,file_gdp_per_capita.shape)
#print(gdp_per_capita_modern.head())

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

#Convert values in column 'year' from string to number
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

#===========================================================MERGING DATA FRAMES



# Left join on the summarid olympics results table and the GDP per capita

olympics_results_gdp_per_capita = olympians_summarised.merge(gdp_per_capita_modern, how = 'left',
                                                             left_on = ['Year', 'ISO'], right_on = ['time', 'geo'],
                                                             suffixes = ('_OLY','_GPC'))

print(olympians_summarised.head(1))
print(gdp_per_capita_modern.head(2))
print(olympics_results_gdp_per_capita.head(3))

#olympics_results_gdp_per_capita['Total_#'] = olympics_results_gdp_per_capita.Gold + olympics_results_gdp_per_capita.Silver + olympics_results_gdp_per_capita.Bronze
# Removing this line since Margins was addeed to the pivot table
olympics_results_gdp_per_capita = olympics_results_gdp_per_capita[["geo","name","time","Bronze","Silver","Gold","All","Income per person","GDP total"]]

#print(olympics_results_gdp_per_capita.iloc[[0,2],:])
#print(olympians_summarised.type)



#print(olympics_results_gdp_per_capita.head(1))
corr = olympics_results_gdp_per_capita.corr()
#print(corr)


#################### Output to CSV
#olympics_results_gdp_per_capita.to_csv(r'C:\Users\Kiran\Google Drive\Learning\03 - UCD - intro to Python\10. Final Project\Data\CSVs from Pandas\olympics_results_gdp_per_capita.csv',index = False, header = True)
#print(olympics_results_gdp_per_capita.head())
#===================Using scatter plot from  PYPLOT
#medals_versus_gdp_per_capita = olympics_results_gdp_per_capita.plot(kind = 'scatter', y = 'All', x = 'GDP total')
#plt.show()

##########################USING SEABORN

sns.set_theme(style='white')
data_for_sns = olympics_results_gdp_per_capita
#print(data_for_sns.head())
sns.set_style('dark')
sns.scatterplot(x =  'Income per person',
               y =  'All',
               hue = 'name',
               size = 'GDP total',
               alpha = 0.8,
               legend = False,
               data = data_for_sns)

plt.show()


#Using Numpy https://stackabuse.com/calculating-pearson-correlation-coefficient-in-python-with-numpy/ to tell the corellation between GDP and olmypic performance