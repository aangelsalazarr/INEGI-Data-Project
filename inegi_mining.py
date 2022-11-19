import os
import matplotlib.pyplot as plt
import seaborn as sns
from data_processor import grab_inegi_data, save_multi_image
import pandas as pd
from datetime import date

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

# mining ids
mining = {
    '5300000005': 'Economic units, sector 21, mining',
    '5300000025': 'Total renumeration, sector 21, mining',
    '5300000035': 'Total gross production, sector 21, mining',
    '5300000045': 'Total stock of fixed assets, sector 21, mining',
    '5300000095': 'Recenue from provision of goods and services, sector 21, '
                  'mining',
    '5300000105': 'Total expenditures for consumption of goods and services, '
                  'sector 21, mining',
    '6207046219': 'Volume of mining production, Gold, by state',
    '6207046220': 'Volume of mining production, Zinc, by state',
    '6207046221': 'Volume of mining production, Copper, by state',
    #'6207046222': 'Volume of mining production, Coke, by state',
    '6207046224': 'Volume of mining production, Silver by state',
    '6207046223': 'Volume of mining production, Lead, by state',
    #'6207046225': 'Volume of mining production, Sulfur, by state',
    #'6207046226': 'Volume of mining production, Baryte, by state',
    #'6207046227': 'Volume of mining production, Fluorite, by state',
    #'6207046230': 'Volume of mining production, Iron Pellets, by state',
    #'6207046231': 'Volume of mining production, Iron Extraction by state',
}

# creating a list of keys
min_keys = list(mining.keys())
geo_keys = list(geos.keys())
bridge_keys = list(bridges.keys())

# turning this into a function moving forward
df = pd.DataFrame(columns=['seriesId'])

# now let's iterate through each key:value pair in dict and create a df
for key in min_keys:

    # grab data
    a = grab_inegi_data(indicator=key, geo=geo_keys[1], bridge=bridge_keys[1])
    df = pd.concat([df, pd.DataFrame(a)])

    # add series id
    if df['seriesId'].isnull:
        df['seriesId'].fillna(key, inplace=True)


# let's drop cols = OBS_EXCEPTION, OBS_SOURCE, & OBS_NOTE
df.drop(['OBS_EXCEPTION', 'OBS_STATUS', 'OBS_SOURCE', 'OBS_NOTE'],
        inplace=True, axis=1)

# lets output our df as a csv file
df.to_csv('./data_files/mx_mining_data.csv', index=False)

# now let's iterate visualizing
for key, value in mining.items():
    plt.figure()
    x = sns.lineplot(data=df[df['seriesId'] == key],
                    x='TIME_PERIOD',
                    y='OBS_VALUE').set(title=value)


# now we will convert our figures into a pdf file
filename = './data_visuals/mexico_mining_data_visuals_'
save_multi_image(filename + currentDate + '.pdf')



