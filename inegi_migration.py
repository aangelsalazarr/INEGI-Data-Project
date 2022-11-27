import os
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rc

from data_processor import *
import pandas as pd
from datetime import date
from decimal import Decimal

# some params related to the framework of output that we will need
rc('mathtext', default='regular')
plt.rcParams["figure.autolayout"] = True
pd.set_option('display.max_columns', None)


# want to load into our environment our api key
simbolico = os.environ.get('inegiKey')
# purpose is to create current date and current year function
today = date.today()
currentDate = today.strftime('%m_%d_%y')
# setting up params for our data_visuals
sns.set(font_scale=0.5)
sns.set_style('dark')

# geo identifier
geos = {'0700':'nacional',
        '07000001': 'not sure what this is'}

# data bridges
bridges = {'BIE':'Bank for Economic Information',
           'BISE':'Bank of Indicators'}

# series id related to migration stats
migration = {
    '6200205255': 'Immigration Population, 5 yrs and over',
    '6200205252': '% international migran pop. headed to other country',
    '6200205262': 'International migration net balance of 5 yrs and over',
    '6200205264': '% international migrant with no destination',
    '6200240349': '% international migration to USA',
    '6200240327': '% of international migration to rest of world',
    '6200240404': '% international migrant pop. due to public '
                  'insecurity/violence',
    '6200240415': '% of international migrant pop. to unspecified countries',
    '6207129645': '% migrant pop. of 5 yrs and over according to: education',
    '6207129646': '% migrant pop. of 5 yrs or over according to: criminal '
                  'insecurity or violence'}

# creating a list of keys
migration_keys = list(migration.keys())
geo_keys = list(geos.keys())
bridge_keys = list(bridges.keys())

# processing our data
df = process_data_by_series(keys=migration_keys, geo=geo_keys[0],
                            bridge=bridge_keys[1])


# cleaning our df
df = clean_data(df=df)

# lets output our df as a csv file
df.to_csv('./data_files/mx_migration_data.csv', index=False)

# visualizing out data
vis_data_lineplot(dict=migration, df=df)


# now we will convert our figures into a pdf file
filename = './data_visuals/mexico_migration_data_visuals_'
save_multi_image(filename + currentDate + '.pdf')

