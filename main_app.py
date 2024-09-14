#%% DATA WRANGLE
import os
import pandas as pd
import plotly.express as px
import numpy as np

# for spyder display
import plotly.io as pio
pio.renderers.default='browser'

#%% Merge dataset No. 1
folder_path = 'data_VCB_1.9_10.9'
file_list = os.listdir(folder_path)
files = [folder_path + '/' + file for file in file_list if file != '.DS_Store']

df1 = pd.DataFrame()
for file in files:
    df_temp = pd.read_csv(file)
    df1 = pd.concat([df1, df_temp], axis='rows')

df1['bank'] = 'vcb'

#%% Merge dataset No. 2
folder_path = 'data_Vietin_10.9_12.9'
file_list = os.listdir(folder_path)
files = [folder_path + '/' + file for file in file_list if file != '.DS_Store']

df2 = pd.DataFrame()
for file in files:
    df_temp = pd.read_csv(file)
    df_temp.drop(columns='Unnamed: 0', inplace=True)
    df2 = pd.concat([df2, df_temp], axis='rows')

df2['bank'] = 'vietin'

#%% All data (up-to-date 12/9/2024)
df = pd.concat([df1, df2], axis='rows')
df = df.reset_index()
df.drop(columns='index')
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

#%% VISUALIZATION

money_array = np.array(df['money'])
upper = np.quantile(money_array, 0.9)

fig = px.histogram(df['money'][df['money'] < upper],
                    nbins=100)
fig.show()