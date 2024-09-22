import os
import pandas as pd

file_list = os.listdir('data_MTTQ TW_Vietin_13.9_15.9')
file_list.remove('.DS_Store')

df = pd.DataFrame()
for file in file_list:
    
    df_temp = pd.read_csv('data_MTTQ TW_Vietin_13.9_15.9/' + file)
    df = pd.concat([df, df_temp], axis='rows')
    
df = df[df['money'].notna()]

# df['money'].apply(lambda row: row if isinstance(row, (float, int)) else row[:-2])

for i, value in enumerate(df['money'].values):
    try:
        float(value)
    except:
        print(value)
        df.iloc[i, 2] = int(value[:-2])
        print(df.iloc[i, 2])
        print("---")
        

df.to_csv('all_page.csv')
