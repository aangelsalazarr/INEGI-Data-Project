import os
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rc
from data_processor import *
import pandas as pd
from datetime import date

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
geos = {'0700': 'nacional',
        '07000001': 'not sure what this is'}

# data bridges
bridges = {'BIE': 'Bank for Economic Information',
           'BISE': 'Bank of Indicators'}

# 0-3 are BISE, 4-6 are BIE, both geos =0700
gdps1 = {
    '6207067864': 'Timely estimate of the quarterly GDP. Annex 1. '
                  'Gross Domestic Product. Originals. Annual Percentage '
                  'Variation',
    '6207067865': 'Timely estimate of the quarterly GDP. Annex 1. '
                  'Gross Domestic Product. Primary Activities. Originals. '
                  'Annual Percentage Variation',
    '6207067866': 'Timely estimate of the quarterly GDP. Annex 1. '
                  'Gross Domestic Product. Tertiary Activities. Originals. '
                  'Annual percentage variation',
    '6207067867': 'Timely estimate of the quarterly GDP. Annex 1. '
                  'Gross Domestic Product. Secondary Activities. '
                  'Annual percentage variation '
}

gdps2 = {
    '494269': 'Producto Interno Bruto, a precios de mercado',
    '494270': 'Impuestos a los productos, netos',
    '494271': 'Valor agregado bruto a precios basicos',
}

gdps = {
    '6207067864': 'Timely estimate of the quarterly GDP. Annex 1. '
                  'Gross Domestic Product. Originals. Annual Percentage '
                  'Variation',
    '6207067865': 'Timely estimate of the quarterly GDP. Annex 1. '
                  'Gross Domestic Product. Primary Activities. Originals. '
                  'Annual Percentage Variation',
    '6207067866': 'Timely estimate of the quarterly GDP. Annex 1. '
                  'Gross Domestic Product. Tertiary Activities. Originals. '
                  'Annual percentage variation',
    '6207067867': 'Timely estimate of the quarterly GDP. Annex 1. '
                  'Gross Domestic Product. Secondary Activities. '
                  'Annual percentage variation ',
    '494269': 'Producto Interno Bruto, a precios de mercado',
    '494270': 'Impuestos a los productos, netos',
    '494271': 'Valor agregado bruto a precios basicos'
}

# creating a list of keys
gdp1_keys = list(gdps1.keys())
gdp2_keys = list(gdps2.keys())
geo_keys = list(geos.keys())
bridge_keys = list(bridges.keys())

# creating first df for first dict
df1 = process_data_by_series(keys=gdp1_keys, geo=geo_keys[0],
                             bridge=bridge_keys[1])

# creating second df for second dict
df2 = process_data_by_series(keys=gdp2_keys, geo=geo_keys[0],
                             bridge=bridge_keys[0])

#
dfs = [df1, df2]

# combing our dfs
df_main = combine_dfs(dfs=dfs)

# cleaning our data
df_main = clean_data(df=df_main)

'''
# TIME_PERIOD -> (1) Year & (2) Quarter
df['year'] = df['TIME_PERIOD'].str[:4]
df['quarter'] = df['TIME_PERIOD'].str[-1:]
df['period'] = df['year'] + '-Q' + df['quarter']
df['period'] = pd.to_datetime(df['period']).dt.strftime('%Y-%m')
'''

# lets output our df as a csv file
df_main.to_csv('./data_files/mx_gdp_data.csv', index=False)

# plotting our data
vis_data_barplot(dict=gdps, df=df_main, start='2015-01')

# now we will convert our figures into a pdf file
filename = './data_visuals/mexico_gdp_data_visuals_'
save_multi_image(filename + currentDate + '.pdf')
