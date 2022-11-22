import os
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rc
from data_processor import grab_inegi_data, save_multi_image
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
geos = {'0700':'nacional',
        '07000001': 'not sure what this is'}

# data bridges
bridges = {'BIE':'Bank for Economic Information',
           'BISE':'Bank of Indicators'}

# 0-3 are BISE, 4-6 are BIE, both geos =0700
gdps_1 = {
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
}

gdps_2 = {
    '494269': 'Producto Interno Bruto, a precios de mercado',
    '494270': 'Impuestos a los productos, netos',
    '494271': 'Valor agregado bruto a precios basicos',
}

# creating a list of keys
gdp_keys1 = list(gdps_1.keys())
gdp_keys2 = list(gdps_2.keys())
geo_keys = list(geos.keys())
bridge_keys = list(bridges.keys())

# turning this into a function moving forward
df = pd.DataFrame(columns=['seriesId'])

# now let's iterate through each key:value pair in dict and create a df
for key in gdp_keys2:

    # grab data
    a = grab_inegi_data(indicator=key, geo=geo_keys[0], bridge=bridge_keys[0])
    df = pd.concat([df, pd.DataFrame(a)])

    # add series id
    if df['seriesId'].isnull:
        df['seriesId'].fillna(key, inplace=True)


# let's drop cols = OBS_EXCEPTION, OBS_SOURCE, & OBS_NOTE
df.drop(['OBS_EXCEPTION', 'OBS_STATUS', 'OBS_SOURCE', 'OBS_NOTE', 'COBER_GEO'],
        inplace=True, axis=1)

# TIME_PERIOD -> (1) Year & (2) Quarter
df['year'] = df['TIME_PERIOD'].str[:4]
df['quarter'] = df['TIME_PERIOD'].str[-1:]
df['period'] = df['year'] + '-Q' + df['quarter']
df['period'] = pd.to_datetime(df['period']).dt.strftime('%Y-%m')


# converting OBS_VALUE to float
df['OBS_VALUE'] = df['OBS_VALUE'].astype(float)

# lets output our df as a csv file
df.to_csv('./data_files/mx_gdp_data.csv', index=False)

# now let's iterate visualizing
for key, value in gdps_2.items():
    plt.figure()
    x = sns.barplot(data=df[(df['seriesId'] == key) & (df['period'] >=
                                                       '2015-01-01')],
                    x='period',
                    y='OBS_VALUE').set(title=value)
    # set the ticks first
    plt.xticks(rotation=90)  # Rotates X-Axis Ticks by 45-degrees

# now we will convert our figures into a pdf file
filename = './data_visuals/mexico_gdp_data_visuals_'
save_multi_image(filename + currentDate + '.pdf')
