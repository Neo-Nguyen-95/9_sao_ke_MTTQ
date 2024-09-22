#%% LIBRARY
import pandas as pd
import os
from datetime import datetime


pd.set_option('display.max_columns', None)
#%% MERGE
def merge_lv1(folder_path):
    file_list = os.listdir(folder_path)
    files = [folder_path + '/' + file for file in file_list if '.csv' in file]

    df = pd.DataFrame()
    for file in files:
        df_temp = pd.read_csv(file)
        df = pd.concat([df, df_temp], axis='rows')

    df['organization'] = folder_path.split('_')[1].lower()
    df['bank'] = folder_path.split('_')[2].lower()
    return df


def merge_lv2(folder_list):
    df = pd.DataFrame()
    for folder_path in folder_list:
        df_temp = merge_lv1(folder_path)
        df = pd.concat([df, df_temp], axis='rows')
    
    # clean money col
    df = df[df['money'].astype(int)>0]
    
    # filter date col
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y').dt.date
    filter_date = datetime(2024,9,8).date()  # the day that storm came
    df = df[df['date'] >= filter_date]
    
    # drop index
    df = df.reset_index()
    df.drop(columns='index', inplace=True)
  
    return df

folder_list = ['database/' + folder for folder in os.listdir('database') if 'data_MTTQ ' in folder]

#%% FUNCTIONAL
class data_module:
    
    def update_data(self):
        df = merge_lv2(folder_list)
        df.to_parquet("database/data_full.parquet", engine="pyarrow")
        
    def load_data(self):
        df = pd.read_parquet("database/data_full.parquet", engine='pyarrow')
        return df

#%%
dataObject = data_module()
dataObject.update_data()
df = dataObject.load_data()