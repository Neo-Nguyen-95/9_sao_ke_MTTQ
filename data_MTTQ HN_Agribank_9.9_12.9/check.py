import pandas as pd

df = pd.read_csv('page_1706_1705.csv')

df = df[df['money'].notna()]

# check
if df['money'].astype(int).sum() - 500000 == (
        df['balance'].iloc[-1] - df['balance'].iloc[0]):
    print('OK')
else: 
    print('error detect')