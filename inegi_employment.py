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
eyos_keys = list(eyos.keys())
geo_keys = list(geos.keys())
bridge_keys = list(bridges.keys())

# now let's iterate through each key:value pair in dict and create a df
df1 = process_data_by_series(keys=eyo_1_keys, geo=geo_keys[0],
                             bridge=bridge_keys[1])
df2 = process_data_by_series(keys=eyo_2_keys, geo=geo_keys[0],
                             bridge=bridge_keys[1])
df3 = process_data_by_series(keys=eyo_3_keys, geo=geo_keys[0],
                             bridge=bridge_keys[1])

# putting all dfs into a list
dfs = [df1, df2, df3]

# concatenating all dfs vertically
df_main = combine_dfs(dfs)
df_main = clean_data(df=df_main)

print(df_main)

# lets output our df as a csv file
df_main.to_csv('./data_files/mx_employment_data.csv', index=False)

vis_data_barplot(dict=eyos, df=df_main)

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

