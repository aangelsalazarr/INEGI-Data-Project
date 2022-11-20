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

# turning this into a function moving forward
df = pd.DataFrame(columns=['seriesId'])

# now let's iterate through each key:value pair in dict and create a df
for key in morts_keys:

    # grab data
    a = grab_inegi_data(indicator=key, geo=geo_keys[0], bridge=bridge_keys[1])
    df = pd.concat([df, pd.DataFrame(a)])

    # add series id
    if df['seriesId'].isnull:
        df['seriesId'].fillna(key, inplace=True)


# let's drop cols = OBS_EXCEPTION, OBS_SOURCE, & OBS_NOTE
df.drop(['OBS_EXCEPTION', 'OBS_STATUS', 'OBS_SOURCE', 'OBS_NOTE'],
        inplace=True, axis=1)

# lets output our df as a csv file
df.to_csv('./data_files/mx_mortality_data.csv', index=False)

# now let's iterate visualizing
for key, value in morts.items():
    plt.figure()
    x = sns.lineplot(data=df[df['seriesId'] == key],
                    x='TIME_PERIOD',
                    y='OBS_VALUE').set(title=value)


# now we will convert our figures into a pdf file
filename = './data_visuals/mexico_mortality_data_visuals_'
save_multi_image(filename + currentDate + '.pdf')