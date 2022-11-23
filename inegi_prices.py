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

# cpi data
prices = {
    '628194': 'hello',
    '628201': 'my',
    '628195': 'name',
    '628198': 'is',
    '628202': 'angel',
    '628205': 'and',
    '628215': 'i',
    '628216': 'like',
    '628219': 'coding',
}

# creating a list of keys
prices_keys = list(prices.keys())
geo_keys = list(geos.keys())
bridge_keys = list(bridges.keys())

# turning this into a function moving forward
df = pd.DataFrame(columns=['seriesId'])

# now let's iterate through each key:value pair in dict and create a df
for key in prices_keys:

    # grab data
    a = grab_inegi_data(indicator=key, geo=geo_keys[0], bridge=bridge_keys[0])
    df = pd.concat([df, pd.DataFrame(a)])

    # add series id
    if df['seriesId'].isnull:
        df['seriesId'].fillna(key, inplace=True)


# let's drop cols = OBS_EXCEPTION, OBS_SOURCE, & OBS_NOTE
df.drop(['OBS_EXCEPTION', 'OBS_STATUS', 'OBS_SOURCE', 'OBS_NOTE', 'COBER_GEO'],
        inplace=True, axis=1)

# period is monthly, so let's convert to date time
df['TIME_PERIOD'] = pd.to_datetime(df['TIME_PERIOD'], format='%Y/%m')

df = df.loc[(df != 0).any(axis=1)]

# converting OBS_VALUE to float
#df['OBS_VALUE'] = df['OBS_VALUE'].astype(float)

print(df)

# lets output our df as a csv file
df.to_csv('./data_files/mx_cpi_data.csv', index=False)

# now let's iterate visualizing
for key, value in prices.items():
    plt.figure()
    x = sns.barplot(data=df[(df['seriesId'] == key) & (df['TIME_PERIOD'] >=
                                                       '2015-01-01')],
                    x='TIME_PERIOD',
                    y='OBS_VALUE').set(title=value)
    # set the ticks first
    plt.xticks(rotation=90)  # Rotates X-Axis Ticks by 45-degrees

# now we will convert our figures into a pdf file
filename = './data_visuals/mexico_cpi_data_visuals_'
save_multi_image(filename + currentDate + '.pdf')

