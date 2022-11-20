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
geos = {'0700':'nacional',  # choose 0700 for ethnicity data
        '07000001': 'not sure what this is'}

# data bridges
bridges = {'BIE':'Bank for Economic Information',
           'BISE':'Bank of Indicators'}  # choose BISE for ethnicity data

# dictionary storing series id and name for ethnicity data
ethns = {
    '1005000039': 'Population 5+ in age who speaks some indigenous language',
    '6200240326': 'Monolingualism rate of the population aged 5 and older '
                  'speakers of Maya',
    '6200240331': 'Zapoteca languages speaking population aged 5 years and '
                  'over',
    '6200240366': 'Population aged 5 years and over who speaks Mayan',
    '6200240386': 'Monolingualism rate of the population aged 5 and older '
                  'speakers of Mixtec languages',
    '6200240433': 'Population aged 5 years and over who speaks mixtecas '
                  'languages',
    '6200240449': 'Rate of monolingualism of the population aged 5 years and '
                  'older who speak Zapoteca',
    '6207019034': 'Monolingualism rate of the population aged 5 years and '
                  'older speaker of indigenous languages',
    '6207019058': '% of population aged 3 years and over that speaks some '
                  'indigenous language',
    '6200240316': '% of population aged 3 yeas and over that speaks some '
                  'indigenous language that does not speak Spanish'
}

# creating a list of keys
ethns_keys = list(ethns.keys())
geo_keys = list(geos.keys())
bridge_keys = list(bridges.keys())

# turning this into a function moving forward
df = pd.DataFrame(columns=['seriesId'])

# now let's iterate through each key:value pair in dict and create a df
for key in ethns_keys:

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
df.to_csv('./data_files/mx_ethnicity_data.csv', index=False)

# now let's iterate visualizing
for key, value in ethns.items():
    plt.figure()
    x = sns.barplot(data=df[df['seriesId'] == key],
                    x='TIME_PERIOD',
                    y='OBS_VALUE').set(title=value)


# now we will convert our figures into a pdf file
filename = './data_visuals/mexico_ethnicity_data_visuals_'
save_multi_image(filename + currentDate + '.pdf')