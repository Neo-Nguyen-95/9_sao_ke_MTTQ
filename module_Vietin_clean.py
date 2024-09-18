import os
import pandas as pd

file_list = os.listdir('data_MTTQ TW_Vietin_13.9_15.9')

df = pd.DataFrame()
for file in file_list:
    df_temp = pd.read_csv('data_MTTQ TW_Vietin_13.9_15.9/' + file)
    df = pd.concat([df, df_temp], axis='rows')