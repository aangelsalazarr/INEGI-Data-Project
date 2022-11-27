import os
import matplotlib.pyplot as plt
import seaborn as sns
from data_processor import *
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
geos = {'0700':'nacional',  # choose 0700 for mortality
        '07000001': 'not sure what this is'}

# data bridges
bridges = {'BIE':'Bank for Economic Information',
           'BISE':'Bank of Indicators'}  # choose BISE for mortality

# mortality index topics
morts = {
    '1002000030':'General deaths',
    '1002000031':'General deaths, men',
    '1002000032':'General deaths, women',
    '1002000034':'Deaths of infants younger than one year',
    '6200002200':'Homicide death rate per 100K inhabitants',
    '6200240338':'Suicides registered',
    '6300000252':'Deaths by homicide, men',
    '6300000268':'Homicide death rate per 100K inhabitants, women',
    '6300000265':'Homicide death rate per 100K inhabitants, men',
    '6300000258':'Deaths by homicide, women'
}

# creating a list of keys
morts_keys = list(morts.keys())
geo_keys = list(geos.keys())
bridge_keys = list(bridges.keys())

# processing our data
df = process_data_by_series(keys=morts_keys, geo=geo_keys[0],
                            bridge=bridge_keys[1])

# cleaning our data
df = clean_data(df=df)

# lets output our df as a csv file
df.to_csv('./data_files/mx_mortality_data.csv', index=False)

# now let's visualize
vis_data_lineplot(dict=morts, df=df)


# now we will convert our figures into a pdf file
filename = './data_visuals/mexico_mortality_data_visuals_'
save_multi_image(filename + currentDate + '.pdf')