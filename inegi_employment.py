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
geos = {'0700': 'nacional',  # this one for employment
        '07000001': 'not sure what this is'}

# data bridges
bridges = {'BIE': 'Bank for Economic Information',
           'BISE': 'Bank of Indicators'}  # this one for employment

# related to job conflicts, job huelgas and last one is total unemployment
# 0-4 are in YYYY, 5-7 are in YYYY/QQ
eyo_1 = {
    '1007000012': 'Conflicto de Trabajo',
    '1007000013': 'Conflicto de Trabajo Solucionados',
    '1007000014': 'Huelgas Estalladas',
    '1007000015': 'Huelgas Solucionadas',
    '5000000002': 'Personal Ocupado Total, Universal Total'
}

# related to sector employment
eyo_2 = {
    '5300000011': 'Personal Ocupado Total, Sector Privado y Paraestatal',
    '5300000012': 'Personal Ocupado Total, Gran Sector 43-46 Comercio',
    '5300000013': 'Personal Ocupado Total, Gran Sector 51, 53, 54, 55, 61, '
                  '62, 71, 72, y 81, Servicios Privados no Financieros',
    '5300000014': 'Personal Ocupado Total, Sector 11, Pesca y Agricultura',
    '5300000015': 'Personal Ocupado Total, Sector 21, Mineria',
    '5300000016': 'Personal Ocupado Total, Sector 22, Electricidad, Agua, '
                  'y Mas',
    '5300000017': 'Personal Ocupado Total, Sector 23, Construccion',
    '5300000018': 'Personal Ocupado Total, Sector 31-33, Industrias '
                  'Manufactureras',
    '5300000019': 'Personal Ocupado Total, Sector 48-49, Transportes',
    '5300000020': 'Personal Ocupado Total, Sector 52, Servicios Financieros y '
                  'de Seguros'
}

# related to informal vs formal on the bases of gender and inlcuded unemployment
eyo_3 = {
    '6200093709': 'Poblacion Ocupada en el Sector Informal, 15 Años y Mas',
    '6200093715': 'Poblacion Ocupada en el Sector Informal, 15 Años y Mas, '
                  'Mujeres',
    '6200093716': 'Poblacion Ocupada en el Sector Informal, 15 Años y Mas, '
                  'Hombres',
    '6200093954': 'Poblacion Ocupada, 15 Años y Mas',
    '6200093950': 'Poblacion Ocupada, 15 Años y Mas, Hombres',
    '6200093956': 'Poblacion Ocupada, 15 Años y Mas, Mujeres',
    '6200093973': 'Poblacion Desocupada, 15 Años y Mas',
    '6200093974': 'Poblacion Desocupada, 15 Años y Mas, Hombres',
    '6200093975': 'Poblacion Desocupada, 15 Años y Mas, Mujeres',
}

eyos = {
    '1007000012': 'Conflicto de Trabajo',
    '1007000013': 'Conflicto de Trabajo Solucionados',
    '1007000014': 'Huelgas Estalladas',
    '1007000015': 'Huelgas Solucionadas',
    '6200093973': 'Poblacion Desocupada, 15 años y mas',
    '6200093974': 'Poblacion Desocupada, 15 años y mas, Hombres',
    '6200093975': 'Poblacion Desocupada, 15 años y mas, Mujeres',
    '5000000002': 'Personal Ocupado Total, Universal Total',
    '5300000011': 'Personal Ocupado Total, Sector Privado y Paraestatal',
    '5300000012': 'Personal Ocupado Total, Gran Sector 43-46 Comercio',
    '5300000013': 'Personal Ocupado Total, Gran Sector 51, 53, 54, 55, 61, '
                  '62, 71, 72, y 81, Servicios Privados no Financieros',
    '5300000014': 'Personal Ocupado Total, Sector 11, Pesca y Agricultura',
    '5300000015': 'Personal Ocupado Total, Sector 21, Mineria',
    '5300000016': 'Personal Ocupado Total, Sector 22, Electricidad, Agua, '
                  'y Mas',
    '5300000017': 'Personal Ocupado Total, Sector 23, Construccion',
    '5300000018': 'Personal Ocupado Total, Sector 31-33, Industrias '
                  'Manufactureras',
    '5300000019': 'Personal Ocupado Total, Sector 48-49, Transportes',
    '5300000020': 'Personal Ocupado Total, Sector 52, Servicios Financieros y '
                  'de Seguros',
    '6200093709': 'Poblacion Ocupada en el Sector Informal, 15 Años y Mas',
    '6200093715': 'Poblacion Ocupada en el Sector Informal, 15 Años y Mas, '
                  'Mujeres',
    '6200093716': 'Poblacion Ocupada en el Sector Informal, 15 Años y Mas, '
                  'Hombres',
    '6200093954': 'Poblacion Ocupada, 15 Años y Mas',
    '6200093950': 'Poblacion Ocupada, 15 Años y Mas, Hombres',
    '6200093956': 'Poblacion Ocupada, 15 Años y Mas, Mujeres'
}

# creating a list of keys
eyo_1_keys = list(eyo_1.keys())
eyo_2_keys = list(eyo_2.keys())
eyo_3_keys = list(eyo_3.keys())
eyos_keys =  list(eyos.keys())
geo_keys = list(geos.keys())
bridge_keys = list(bridges.keys())

# turning this into a function moving forward
df1 = pd.DataFrame(columns=['seriesId'])
df2 = pd.DataFrame(columns=['seriesId'])
df3 = pd.DataFrame(columns=['seriesId'])

# now let's iterate through each key:value pair in dict and create a df
for key in eyo_1_keys:

    # grab data
    a = grab_inegi_data(indicator=key, geo=geo_keys[0], bridge=bridge_keys[1])
    df1 = pd.concat([df1, pd.DataFrame(a)])

    # add series id
    if df1['seriesId'].isnull:
        df1['seriesId'].fillna(key, inplace=True)

    # dropping all empty cells
    if df1['OBS_VALUE'].isnull:
        df1['OBS_VALUE'].fillna('NA', inplace=True)

for key in eyo_2_keys:

    # grab data
    b = grab_inegi_data(indicator=key, geo=geo_keys[0], bridge=bridge_keys[1])
    df2 = pd.concat([df2, pd.DataFrame(b)])

    # add series id
    if df2['seriesId'].isnull:
        df2['seriesId'].fillna(key, inplace=True)

    # dropping all empty cells
    if df2['OBS_VALUE'].isnull:
        df2['OBS_VALUE'].fillna('NA', inplace=True)


for key in eyo_3_keys:

    # grab data
    c = grab_inegi_data(indicator=key, geo=geo_keys[0], bridge=bridge_keys[1])
    df3 = pd.concat([df3, pd.DataFrame(c)])

    # add series id
    if df3['seriesId'].isnull:
        df3['seriesId'].fillna(key, inplace=True)

    # dropping all empty cells
    if df3['OBS_VALUE'].isnull:
        df3['OBS_VALUE'].fillna('NA', inplace=True)

# putting all dfs into a list
dfs = [df1, df2, df3]

# concatenating all dfs vertically
df_main = combine_dfs(dfs)

# dropping the columns we do not need
df_main.drop(['OBS_EXCEPTION', 'OBS_STATUS', 'OBS_SOURCE', 'OBS_NOTE',
              'COBER_GEO'],
             inplace=True, axis=1)

# getting rid of any empty cells
df_main = df_main[df_main['OBS_VALUE'] != 'NA']

df_main.reset_index(inplace=True)
df_main['OBS_VALUE'] = df_main['OBS_VALUE'].astype(float)


# lets output our df as a csv file
df_main.to_csv('./data_files/mx_employment_data.csv', index=False)
print(df_main)


# now let's iterate visualizing
for key, value in eyos.items():
    plt.figure()
    x = sns.barplot(data=df_main[(df_main['seriesId'] == key)],
                    x='TIME_PERIOD',
                    y='OBS_VALUE').set(title=value)
    # set the ticks first
    plt.xticks(rotation=90)  # Rotates X-Axis Ticks by 45-degrees

# now we will convert our figures into a pdf file
filename = './data_visuals/mexico_employment_data_visuals_'
save_multi_image(filename + currentDate + '.pdf')

'''
# TIME_PERIOD -> (1) Year & (2) Quarter
df['year'] = df['TIME_PERIOD'].str[:4]
df['quarter'] = df['TIME_PERIOD'].str[-1:]
df['period'] = df['year'] + '-Q' + df['quarter']
df['period'] = pd.to_datetime(df['period']).dt.strftime('%Y-%m')


'''
