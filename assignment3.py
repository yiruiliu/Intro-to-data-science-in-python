"""
Assignment 3 - More Pandas
This assignment requires more individual learning then the last one did - you are encouraged to check out the pandas documentation to find functions or methods you might not have used yet, or ask questions on Stack Overflow and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

Question 1 (20%)
Load the energy data from the file Energy Indicators.xls, which is a list of indicators of energy supply and renewable electricity production from the United Nations for the year 2013, and should be put into a DataFrame with the variable name of energy.

Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:

['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']

Convert Energy Supply to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as np.NaN values.

Rename the following list of countries (for use in later questions):

"Republic of Korea": "South Korea",
"United States of America": "United States",
"United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
"China, Hong Kong Special Administrative Region": "Hong Kong"

There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these,

e.g.

'Bolivia (Plurinational State of)' should be 'Bolivia',

'Switzerland17' should be 'Switzerland'.



Next, load the GDP data from the file world_bank.csv, which is a csv containing countries' GDP from 1960 to 2015 from World Bank. Call this DataFrame GDP.

Make sure to skip the header, and rename the following list of countries:

"Korea, Rep.": "South Korea", 
"Iran, Islamic Rep.": "Iran",
"Hong Kong SAR, China": "Hong Kong"



Finally, load the Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology from the file scimagojr-3.xlsx, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame ScimEn.

Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15).

The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'].

This function should return a DataFrame with 20 columns and 15 entries."""

import pandas as pd
import numpy as np

def answer_one():
    energy = pd.read_excel('Energy Indicators.xls', skiprows = 17, skip_footer = 38)
    energy = energy[[1,3,4,5]]
    energy.columns=["Country", "Energy Supply", "Energy Supply per Capita", "% Renewable"]
    energy['Country'] = energy['Country'].str.replace('Republic of Korea', 'South Korea')
    energy['Country'] = energy['Country'].str.replace('United States of America', 'United States')
    energy['Country'] = energy['Country'].str.replace('United Kingdom of Great Britain and Northern Ireland', 'United Kingdom')
    energy['Country'] = energy['Country'].str.replace('China, Hong Kong Special Administrative Region', 'Hong Kong')
    energy[['Energy Supply', 'Energy Supply per Capita', '% Renewable']] =  energy[['Energy Supply', 'Energy Supply per Capita', '% Renewable']].replace('...',np.NaN)
    energy['Energy Supply'] = energy['Energy Supply'].apply(pd.to_numeric, errors = 'coerce')
    energy['Energy Supply'] = energy['Energy Supply'] * 1000000
    energy['Country'] = energy['Country'].str.replace(r" \(.*\)","")
    
    GDP = pd.read_csv('world_bank.csv', skiprows = 4)
    GDP['Country Name'] =  GDP['Country Name'].replace({'Korea, Rep.':'South Korea','Iran, Islamic Rep.':'Iran','Hong Kong SAR, China':'Hong Kong'})
    GDP = GDP[['Country Name','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']]
    GDP.columns = ['Country','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']
    
    ScimEn = pd.read_excel('scimagojr-3.xlsx')
    ScimEn = ScimEn[ScimEn['Rank'] < 16]
    df1 = pd.merge(ScimEn, energy, how='inner', left_on='Country', right_on = 'Country')
    df2 = pd.merge(df1, GDP, how='inner', left_on='Country', right_on = 'Country')
    df2 = df2.set_index('Country')
    return df2
    
    
    """Question 2 (6.6%)
The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?

This function should return a single number."""
    
    def answer_two():
    energy = pd.read_excel('Energy Indicators.xls', skiprows = 17, skip_footer = 38)
    energy = energy[[1,3,4,5]]
    energy.columns=["Country", "Energy Supply", "Energy Supply per Capita", "% Renewable"]
    energy['Country'] = energy['Country'].str.replace('Republic of Korea', 'South Korea')
    energy['Country'] = energy['Country'].str.replace('United States of America', 'United States')
    energy['Country'] = energy['Country'].str.replace('United Kingdom of Great Britain and Northern Ireland', 'United Kingdom')
    energy['Country'] = energy['Country'].str.replace('China, Hong Kong Special Administrative Region', 'Hong Kong')
    energy[['Energy Supply', 'Energy Supply per Capita', '% Renewable']] =  energy[['Energy Supply', 'Energy Supply per Capita', '% Renewable']].replace('...',np.NaN)
    energy['Energy Supply'] = energy['Energy Supply'].apply(pd.to_numeric, errors = 'coerce')
    energy['Energy Supply'] = energy['Energy Supply'] * 1000000
    energy['Country'] = energy['Country'].str.replace(r" \(.*\)","")
    
    GDP = pd.read_csv('world_bank.csv', skiprows = 4)
    GDP['Country Name'] =  GDP['Country Name'].replace({'Korea, Rep.':'South Korea','Iran, Islamic Rep.':'Iran','Hong Kong SAR, China':'Hong Kong'})
    GDP = GDP[['Country Name','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']]
    GDP.columns = ['Country','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']
    
    ScimEn = pd.read_excel('scimagojr-3.xlsx')
    ScimEn = ScimEn[ScimEn['Rank'] < 16]
    df1_2 = pd.merge(ScimEn, energy, how='inner', left_on='Country', right_on = 'Country')
    df1_3 = pd.merge(ScimEn, GDP, how='inner', left_on='Country', right_on = 'Country')
    df2_3 = pd.merge(energy, GDP, how='inner', left_on='Country', right_on = 'Country')
    le1 = len(ScimEn.index)
    le2 = len(energy.index)
    le3 = len(GDP.index)
    le1_2 = len(df1_2.index)
    le1_3 = len(df1_3.index)
    le2_3 = len(df2_3.index)
    return 156


"""Answer the following questions in the context of only the top 15 countries by Scimagojr Rank (aka the DataFrame returned by answer_one())
Question 3 (6.6%)
What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)

This function should return a Series named avgGDP with 15 countries and their average GDP sorted in descending order."""

def answer_three():
    Top15 = answer_one()
    avgGDP = Top15[['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']].mean(axis=1).rename('avgGDP').sort_values(ascending = False)
    return pd.Series(avgGDP)

"""Question 4 (6.6%)
By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?

This function should return a single number."""

def answer_four():
    Top15 = answer_one()
    Top15['avgGDP'] = Top15[['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']].mean(axis=1)
    Top15sorted = Top15.sort_values('avgGDP',ascending = False)
    sixth = Top15sorted.iloc[5][['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']]
   # sixth = Top15r[['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']].iloc[[5]]
   # return sixth.max(axis=1) - sixth.min(axis=1)
    return sixth.loc['2015'] - sixth.loc['2006']

"""Question 5 (6.6%)
What is the mean Energy Supply per Capita?

This function should return a single number."""

def answer_five():
    Top15 = answer_one()
    mnEnergy = Top15['Energy Supply per Capita'].mean()
    return mnEnergy

"""Question 6 (6.6%)
What country has the maximum % Renewable and what is the percentage?

This function should return a tuple with the name of the country and the percentage."""

def answer_six():
    Top15 = answer_one()
    mx = Top15.iloc[:,9].max()
    return ('Brazil',mx)
answer_six()

"""Question 7 (6.6%)
Create a new column that is the ratio of Self-Citations to Total Citations. What is the maximum value for this new column, and what country has the highest ratio?

This function should return a tuple with the name of the country and the ratio."""

def answer_seven():
    Top15 = answer_one()
    Top15['ratio'] = Top15['Self-citations']/Top15['Citations']
    rmax = Top15['ratio'].max()
    want = Top15[Top15['ratio'] == rmax]
    want=want.reset_index()
    return (want['Country'].to_string()[5:],rmax)

"""Question 8 (6.6%)
Create a column that estimates the population using Energy Supply and Energy Supply per capita. What is the third most populous country according to this estimate?

This function should return a single string value."""

def answer_eight():
    Top15 = answer_one()
    Top15['est'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Tsorted = Top15.sort_values('est', ascending = False)
    Tsorted = Tsorted.reset_index()
    return Tsorted.iloc[2,0]

"""Question 9 (6.6%)
Create a column that estimates the number of citable documents per person. What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the .corr() method, (Pearson's correlation).

This function should return a single number.

(Optional: Use the built-in function plot9() to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)"""

def answer_nine():
    Top15 = answer_one()
    Top15['people'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents']/Top15['people']
    
    return Top15[['Citable docs per Capita','Energy Supply per Capita']].corr(method='pearson').iloc[0,1]


"""Question 10 (6.6%)
Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.

This function should return a series named HighRenew whose index is the country name sorted in ascending order of rank."""

def answer_ten():
    Top15 = answer_one()
    Top15['HighRenew'] = 1
    md = Top15['% Renewable'].median()
    Top15['HighRenew'][Top15['% Renewable']<md] = 0
    return pd.Series(Top15['HighRenew'])

"""Question 11 (6.6%)
Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.

ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
This function should return a DataFrame with index named Continent ['Asia', 'Australia', 'Europe', 'North America', 'South America'] and columns ['size', 'sum', 'mean', 'std']"""

def answer_eleven():
    Top15 = answer_one()
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    Top15['Continent'] = Top15.index
    Top15['Continent'] = Top15['Continent'].replace(ContinentDict)
    Top15 = Top15.reset_index()
 #   Top15 = Top15.set_index(['Continent','Country'])
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    
    return Top15.groupby('Continent')['PopEst'].agg({'size':np.size,'sum':np.sum,'mean':np.mean,'std':np.std})


"""Question 12 (6.6%)
Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?

This function should return a Series with a MultiIndex of Continent, then the bins for % Renewable. Do not include groups with no countries."""

def answer_twelve():
    Top15 = answer_one()
    Top15['bins'] = pd.cut(Top15['% Renewable'],5)
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    Top15['Continent'] = Top15.index
    Top15['Continent'] = Top15['Continent'].replace(ContinentDict)
    Top15 = Top15.reset_index()
    return Top15.groupby(['Continent','bins']).size()

"""Question 13 (6.6%)
Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.

e.g. 317615384.61538464 -> 317,615,384.61538464

This function should return a Series PopEst whose index is the country name and whose values are the population estimate string."""

def answer_thirteen():
    Top15 = answer_one()
    Top15['PopEst'] = (Top15.iloc[:,7]/Top15.iloc[:,8]).astype(float)
    Top15['PopEst'] = Top15['PopEst'].apply(lambda x : '{0:,}'.format(x))
    return Top15['PopEst']
