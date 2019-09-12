
"""Assignment 4 - Hypothesis Testing
This assignment requires more individual learning than previous assignments - you are encouraged to check out the pandas documentation to find functions or methods you might not have used yet, or ask questions on Stack Overflow and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

Definitions:

A quarter is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
A recession is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
A recession bottom is the quarter within a recession which had the lowest GDP.
A university town is a city which has a high percentage of university students compared to the total population of the city.
Hypothesis: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (price_ratio=quarter_before_recession/recession_bottom)

The following data files are available for this assignment:

From the Zillow research data site there is housing data for the United States. In particular the datafile for all homes at a city level, City_Zhvi_AllHomes.csv, has median home sale prices at a fine grained level.
From the Wikipedia page on college towns is a list of university towns in the United States which has been copy and pasted into the file university_towns.txt.
From Bureau of Economic Analysis, US Department of Commerce, the GDP over time of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file gdplev.xls. For this assignment, only look at GDP data from the first quarter of 2000 onward.
Each function in this assignment below is worth 10%, with the exception of run_ttest(), which is worth 50%."""


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    df = pd.read_table('university_towns.txt', header = None)
    state = str(df.iloc[0].values)[2:-8]
    rist = []
    for i in range(1,len(df)):
        if '[edit]' not in str(df.iloc[i].values):
            rist.append([state,str(df.iloc[i].values)[2:-1]])
        else:
            state = str(df.iloc[i].values)[2:-8]
    
    df1 = pd.DataFrame(rist,columns=['State','RegionName'])
    df1['RegionName'] = df1['RegionName'] + '}'
    df1['RegionName'] = df1['RegionName'].str.replace(r"\(.*\}","")
    df1['RegionName'] = df1['RegionName'].str.replace(r"'","")
    df1['RegionName'] = df1['RegionName'].str[:-1]
    df1['RegionName'][(df1['RegionName'].str[0] < 'A') | (df1['RegionName'].str[0] > 'Z')] = df1['RegionName'][(df1['RegionName'].str[0] < 'A') | (df1['RegionName'].str[0] > 'Z')].str[1:]
    return df1
  
  def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    gdp_raw = pd.read_excel('gdplev.xls')
    gdp = gdp_raw[['Unnamed: 4','Unnamed: 6']]
    gdp.columns = ['Year','GDP_chain']
    gdp = gdp[gdp['Year'] >= '2000q1']
    gdp = gdp.drop([1])
    gdp = gdp.reset_index(drop = True)
    for i in range(0,len(gdp)-2):
        if (gdp['GDP_chain'].iloc[i] > gdp['GDP_chain'].iloc[i + 1]) and (gdp['GDP_chain'].iloc[i + 1] > gdp['GDP_chain'].iloc[i + 2]) and (gdp['GDP_chain'].iloc[i + 2] < gdp['GDP_chain'].iloc[i + 3]) and (gdp['GDP_chain'].iloc[i + 3] < gdp['GDP_chain'].iloc[i + 4]):
            find = i
           # print(find)
            break
    return gdp['Year'].iloc[find - 1]
  
  def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    gdp_raw = pd.read_excel('gdplev.xls')
    gdp = gdp_raw[['Unnamed: 4','Unnamed: 6']]
    gdp.columns = ['Year','GDP_chain']
    gdp = gdp[gdp['Year'] >= '2000q1']
    gdp = gdp.drop([1])
    gdp = gdp.reset_index(drop = True)
    for i in range(0,len(gdp)-2):
        if (gdp['GDP_chain'].iloc[i] > gdp['GDP_chain'].iloc[i + 1]) and (gdp['GDP_chain'].iloc[i + 1] > gdp['GDP_chain'].iloc[i + 2]) and (gdp['GDP_chain'].iloc[i + 2] < gdp['GDP_chain'].iloc[i + 3]) and (gdp['GDP_chain'].iloc[i + 3] < gdp['GDP_chain'].iloc[i + 4]):
            find = i
            break
    return gdp['Year'].iloc[find + 4]
  
  def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    gdp_raw = pd.read_excel('gdplev.xls')
    gdp = gdp_raw[['Unnamed: 4','Unnamed: 6']]
    gdp.columns = ['Year','GDP_chain']
    gdp = gdp[gdp['Year'] >= '2000q1']
    gdp = gdp.drop([1])
    gdp = gdp.reset_index(drop = True)
    for i in range(0,len(gdp)-2):
        if (gdp['GDP_chain'].iloc[i] > gdp['GDP_chain'].iloc[i + 1]) and (gdp['GDP_chain'].iloc[i + 1] > gdp['GDP_chain'].iloc[i + 2]) and (gdp['GDP_chain'].iloc[i + 2] < gdp['GDP_chain'].iloc[i + 3]) and (gdp['GDP_chain'].iloc[i + 3] < gdp['GDP_chain'].iloc[i + 4]):
            find = i
            break
    return gdp['Year'].iloc[find + 2]
  
  def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    housedf = pd.read_csv('City_Zhvi_AllHomes.csv')
    
    l = range(0,49)
    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
    housedf.replace({'State':states}, inplace = True)
    housedf = housedf.set_index(['State','RegionName'])
    housedf = housedf.drop(housedf.columns[[l]],axis = 1)
    housedf = housedf.groupby(pd.PeriodIndex(housedf.columns, freq='q'), axis=1).mean()
    return housedf
  
  def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    univ = get_list_of_university_towns()
    start = get_recession_start()
    end = get_recession_end()
    bottom = get_recession_bottom()
    housedf = convert_housing_data_to_quarters()
    
    price_start = housedf[start]
    price_end = housedf[end]
    ratio = price_start.divide(price_end)
    
    univ = univ.set_index(['State','RegionName'])
    ratio_univ = ratio[list(univ.index)].dropna()

    ratio_not_univ = ratio.loc[list(set(housedf.index) - set(ratio_univ.index))].dropna()
    stat, p = tuple(ttest_ind(ratio_univ, ratio_not_univ))
    
    if stat < 0:
        result = "university town"
    else:
        result = "non-university town"
   
    return (p < 0.01, p, result)
