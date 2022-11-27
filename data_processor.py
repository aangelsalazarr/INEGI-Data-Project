import requests
import json
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# want to load into our environment our api key
simbolico = os.environ.get('inegiKey')


def grab_inegi_data(indicator, geo, bridge):
    # calling api
    base = 'https://en.www.inegi.org.mx/app/api/indicadores/desarrolladores/' \
           'jsonxml/INDICATOR/'
    ind = indicator + '/'  # id indicator, list(mining.keys())[6]
    lang = 'en' + '/'  # or 'es' for spanish language
    geo_id = geo + '/'  # geographic area, list(geos.keys())[1]
    recents = 'false/'  # or 'false/' for if you want historical data?
    data_bridge = bridge + '/'  # list(bridges.keys())[1]
    v = '2.0/'  # not sure what else you could put here for version lol
    token = simbolico + '?type=json'  # api key
    # url segments concatenated
    url = base + ind + lang + geo_id + recents + data_bridge + v + token

    # response var
    response = requests.get(url=url)
    data = response.json()
    entries = data['Series'][0]['OBSERVATIONS']
    df = pd.DataFrame(data=entries)

    return df


def process_data_by_series(keys, geo, bridge):
    # empty df with seriesId column
    df = pd.DataFrame(columns=['seriesId'])

    for key in keys:

        # grabbing data
        a = grab_inegi_data(indicator=key, geo=geo, bridge=bridge)
        df = pd.concat([df, pd.DataFrame(a)])

        # add seriesId
        if df['seriesId'].isnull:
            df['seriesId'].fillna(key, inplace=True)

        # dropping all empty sells
        if df['OBS_VALUE'].isnull:
            df['OBS_VALUE'].fillna('NA', inplace=True)

    return df


def clean_data(df):
    # dropping the cols listed below as they don't hold relevant data
    df.drop(['OBS_EXCEPTION', 'OBS_STATUS', 'OBS_SOURCE', 'OBS_NOTE',
             'COBER_GEO'], inplace=True, axis=1)

    # dropping rows with cells = NA
    df = df[df['OBS_VALUE'] != 'NA']
    df = df[df['OBS_VALUE'] != '']

    # resetting our index
    df.reset_index(inplace=True)

    # changing obs_value to float
    df['OBS_VALUE'] = df['OBS_VALUE'].astype(float)

    return df


def vis_data_barplot(dict, df, start='1901-01'):
    for key, value in dict.items():
        plt.figure()
        x = sns.barplot(data=df[(df['seriesId'] == key) & (df['TIME_PERIOD']
                                                           >= str(start))],
                        x='TIME_PERIOD',
                        y='OBS_VALUE',
                        color='maroon').set(title=value)

        # rotate our xticks 90 degrees
        plt.xticks(rotation=90)


def vis_data_lineplot(dict, df, start='1901-01'):
    for key, value in dict.items():
        plt.figure()

        x = sns.barplot(data=df[(df['seriesId'] == key) & (df['TIME_PERIOD']
                                                           >= str(start))]
                        ,
                        x='TIME_PERIOD',
                        y='OBS_VALUE', color='maroon').set(title=value)

        # rotate our xticks 90 degrees
        plt.xticks(rotation=90)


def combine_dfs(dfs):
    combined_df = pd.concat(dfs, axis=0, ignore_index=True)

    return combined_df


def save_multi_image(filename):
    pp = PdfPages(filename)
    fig_nums = plt.get_fignums()
    figs = [plt.figure(n) for n in fig_nums]
    for fig in figs:
        fig.savefig(pp, format='pdf')
    pp.close()
