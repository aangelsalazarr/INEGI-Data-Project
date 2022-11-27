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
geos = {'0700':'nacional',
        '07000001': 'not sure what this is'}

# data bridges
bridges = {'BIE':'Bank for Economic Information',
           'BISE':'Bank of Indicators'}

# cpi data
prices = {
    '628194': 'Indice Nacional de Precios al Sonsumidor, Base Segunda '
              'Quincena de Julio de 2018=100, Indice General',
    '628195': 'Indice Nacional de Precios al Sonsumidor, Base Segunda '
              'Quincena de Julio de 2018=100, Indice General, Subyacente Total',
    '628201': 'Indice Nacional de Precios al Sonsumidor, Base Segunda '
              'Quincena de Julio de 2018=100, Indice General, Subyacente Total',
    '628198': 'Indice Nacional de Precios al Sonsumidor, Base Segunda '
              'Quincena de Julio de 2018=100, Inflacion Mensual',
    '628202': 'Indice Nacional de Precios al Sonsumidor, Base Segunda '
              'Quincena de Julio de 2018=100, Inflacion Mensual, Subyacente '
              'Total',
    '628205': 'Indice Nacional de Precios al Sonsumidor, Base Segunda '
              'Quincena de Julio de 2018=100, Inflacion Mensual, No Subyacente '
              'Total',
    '628215': 'Indice Nacional de Precios al Sonsumidor, Base Segunda '
              'Quincena de Julio de 2018=100, Inflacion Acumulada Anual, '
              'Indice General',
    '628216': 'Indice Nacional de Precios al Sonsumidor, Base Segunda '
              'Quincena de Julio de 2018=100, Inflacion Acumulada Anual, '
              'Subyacente Total',
    '628219': 'Indice Nacional de Precios al Sonsumidor, Base Segunda '
              'Quincena de Julio de 2018=100, Inflacion Acumulada Anual, '
              'Subyacente Total',
}

# creating a list of keys
prices_keys = list(prices.keys())
geo_keys = list(geos.keys())
bridge_keys = list(bridges.keys())

# processing our data
df = process_data_by_series(keys=prices_keys,
                            geo=geo_keys[0],
                            bridge=bridge_keys[0])

# let's clean our data
df = clean_data(df=df)

# lets output our df as a csv file
df.to_csv('./data_files/mx_cpi_data.csv', index=False)

vis_data_lineplot(dict=prices, df=df, start='2020-01')

'''
# period is monthly, so let's convert to date time
df['TIME_PERIOD'] = pd.to_datetime(df['TIME_PERIOD'],
                                   format='%Y/%m').dt.strftime('%Y-%m')
                                   
'''

# now we will convert our figures into a pdf file
filename = './data_visuals/mexico_cpi_data_visuals_'
save_multi_image(filename + currentDate + '.pdf')