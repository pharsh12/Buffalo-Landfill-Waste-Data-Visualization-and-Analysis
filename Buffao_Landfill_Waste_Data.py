# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 18:41:08 2018

@author: hp
"""

#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata
import matplotlib.pyplot as plt

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.buffalony.gov", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.buffalony.gov,
#                  MyAppToken,
#                  userame="user@example.com",
#                  password="AFakePassword")
# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("5b4n-rmfi", limit=2000)
results

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)


# Re-structuring of the data.
# The date format is string so we have converted it to numeric form and the date format is changed to YYYY.
results_df= results_df.drop(['month'], axis=1)
Results_df1= results_df.drop(['type'],axis=1)
Results_df1= Results_df1.drop(['total_in_tons'],axis=1)
Results_df1['date'] = pd.to_datetime(Results_df1['date']).apply(lambda x:x.strftime('%Y'))
Results_df1['date'] = Results_df1['date'].apply(pd.to_numeric)

# We have created a separate dataframe with unique years only(Removed duplicates)
date= Results_df1.drop_duplicates(['date'])


# Pie chart for types of waste
# To create a pie chart and to analyze percentage of waste, we used pivot table function.

results_df2 = results_df.drop(['date'], axis=1)
results_df2['total_in_tons'] = results_df2['total_in_tons'].apply(pd.to_numeric)

# This pivot table indicate the type of waste and the total waste diverted from the landfill till current year for the same type of waste.

pivot_pie = pd.pivot_table(results_df2,index=['type'])

# To analyze the pattern of yearly wastes diverted from the landfill for the top 5 contributor in the waste we have used the line graph.
# Formed a dataframe containing the type of wastes and total in tons in terms of percentage.
values = ( pivot_pie['total_in_tons'] ) 
total= (sum(values))
val = ((values/total)*100.0)
val = val.reindex(pivot_pie['total_in_tons'].sort_values(ascending=False).index)
val = val.reset_index()

# To plot legends for the pie chart we have created a separate dataframe x
x = results_df.drop_duplicates(['type'])
x = x.sort_values('type')

#Pie chart ploting
plt.figure(figsize=(12,12))
explode = (0,0,0,0,.3,0,0,0,0.3,0,0,0)
color = ('b','g','orange','m','r','k','cyan','indigo','peru','yellow','violet','lime')
plt.pie(pivot_pie['total_in_tons'],  autopct='%.2f%%', explode= explode, pctdistance = 1.15, colors= color)
plt.rcParams['font.size']=10
plt.legend(labels = x['type'], loc='left',bbox_to_anchor=(0,0.5), prop={'size':12})
plt. title ('Percentage Distribution of Different Type of Waste', fontsize = 15)
plt.savefig('Percentage_Distribution_of_Different_Type_of_Waste.pdf', bbox_inches ='tight')
plt.show()

# To plot the line graph use the following code.
# This plot will indicate yearly tonnage diverted from landfill for the top 5 wastes contributor.
# labels=[]
z=0
for i in range(0,5):
    waste_type = results_df[results_df['type'] == val['type'][i]]
    waste_type = waste_type.drop(['type'], axis=1)
    waste_type['date'] = pd.to_datetime(waste_type['date']).apply(lambda x:x.strftime('%Y'))
    waste_type['total_in_tons'] = waste_type['total_in_tons'].apply(pd.to_numeric)
    pivot1 = pd.pivot_table(waste_type,index=['date'])
    #labels.append(val['type'][i])
    
    plt.ylabel ('Wastage in tons')
    plt.xlabel ('Year')
    plt.title ('Top Five Waste Contributors', fontsize=15)
    plt.plot(date['date'],pivot1, label = val['type'][i])
    plt.legend(loc='left',bbox_to_anchor=(1.5,1))
    i=z+1
    plt.savefig('Top_Five_Waste_Contributors.pdf',bbox_inches ='tight')
plt.show()    