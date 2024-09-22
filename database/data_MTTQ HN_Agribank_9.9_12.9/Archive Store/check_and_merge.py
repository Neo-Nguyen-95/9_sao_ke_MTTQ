#%% Library
import pandas as pd
pd.set_option('display.max_columns', None)
import os
os.chdir('/Users/dungnguyen/Desktop/Data Science off/Python Programming/2. Practice Project/9_sao_ke_MTTQ/data_MTTQ HN_Agribank_9.9_12.9')

#%%
folder_check = os.listdir()
file_list = [file for file in folder_check if '.csv' in file]
file_list = sorted(file_list)

def check_file(df):
    total_amount = df['money'].sum() - df.iloc[0, 1]
    balance_increase = df['balance'].iloc[-1] - df['balance'].iloc[0]
    
    # check
    if total_amount == balance_increase:
        return 'ok'
    else:
        return 'error'
     
#%%
def check_line(df):
    for i in range(len(df)-1):
        balance_start = df.iloc[i, 3]
        balance_next = df.iloc[i+1, 3]
        money_add = df.iloc[i+1, 1]
        
        if balance_next - balance_start != money_add:
            print(f'Error before row: {i+3}')

#%%
df = pd.DataFrame()

for file in file_list:
    df_temp = pd.read_csv(file)
    
    try:
        df_temp['money'] = df_temp['money'].astype(float)
        df_temp['balance'] = df_temp['balance'].astype(float)
    except:
        print(file)
    
    if check_file(df_temp) == 'error':
        print(file)
        check_line(pd.read_csv(file))
        break
    
    df = pd.concat([df, df_temp], axis='rows')

check_line(df)
print(check_file(df))

df.to_csv('agribank_verified.csv')
    
    
    
    
    
    
    
    
    
    