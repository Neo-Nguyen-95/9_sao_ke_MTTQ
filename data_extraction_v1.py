#%% LIBRARY
import pdfplumber
import pandas as pd
import re

file_path = 'data/sao_ke_MTTQ_p1_3.pdf'
#%%
def extract_table(file_path):
    with pdfplumber.open(file_path) as pdf:
        all_tables = []
        all_texts = ''
        for page in pdf.pages:
            tables = page.extract_table()
            all_tables.extend(tables)
            
            all_texts += page.extract_text()
            
    return all_tables, all_texts

all_tables, all_texts = extract_table(file_path)

#%% I. EXTRACT DATE & CASH
dates, docs, money_texts, moneys = [] , [], [], []

for index, content in enumerate(all_tables):
    if index % 2 == 1:
        dates.extend(content[0].splitlines()[0::2])
        docs.extend(content[0].splitlines()[1::2])
        money_texts.extend(content[2].splitlines())
        moneys.extend(content[2].replace('.','').splitlines())

# verification
if (len(dates)==len(docs)) & (len(docs)==len(moneys)):
    print(f'Number of transaction: {len(dates)}')
    print("Everything's fine")

#%% II. EXTRACT CONTENT
def clean_text(text):
    text = re.sub(r'Số CT/ Doc No|Postal', 'break_point', text)
    text = text.split('break_point')
    
    content_text = ''
    for index, content in enumerate(text):
        if index % 2 == 1:
            content_text += content
            
    pattern = '|'.join(re.escape(doc) for doc in set(docs))  + '|' + \
            '|'.join(re.escape(money_text) for money_text in money_texts)
            
    content_text = re.sub(pattern, '', content_text)
    
    pattern = '|'.join(re.escape(date) for date in set(dates))
    
    content_text = re.sub(pattern, 'break_point', content_text)
    
    content_text = content_text.replace('\n', ' ')
    content_text = content_text.split('break_point')
    content_text = [content.strip().replace('  ', ' ') for content in content_text]
    
    return content_text

content_text = clean_text(all_texts)

print(f'Number of content: {len(content_text[1:])}')

#%% MERGE

df = pd.DataFrame({'date': dates,
                   'amount': moneys,
                   'content': content_text[1:]})

print(df.head())












        