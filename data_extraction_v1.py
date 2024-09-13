#%% LIBRARY
import pdfplumber
import pandas as pd

file_path = 'data/sao_ke_MTTQ_p1_3.pdf'
#%% I. EXTRACT DATE % CASH
def extract_table(file_path):
    with pdfplumber.open(file_path) as pdf:
        all_tables = []
        for page in pdf.pages:
            tables = page.extract_table()
            all_tables.extend(tables)
            
    return all_tables

data1 = extract_table(file_path)
#%%
dates = []
docs = []
money_texts = []
moneys = []

for index, content in enumerate(data1):
    if index%2==1:
        dates.extend(content[0].splitlines()[0::2])
        docs.extend(content[0].splitlines()[1::2])
        money_texts.extend(content[2].splitlines())
        moneys.extend(content[2].replace('.','').splitlines())

# verification
if (len(dates)==len(docs)) & (len(docs)==len(moneys)):
    print(f'Number of transaction: {len(dates)}')
    print("Everything's fine")
#####------- DONE SO FAR
#%% II. EXTRACT CONTENT
def extract_text(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

text = extract_text(file_path)

text = (text
        .replace('Số CT/ Doc No', 'break_point').replace('Postal', 'break_point')
        )

data2 = text.split('break_point')

content_text = ''

for index, content in enumerate(data2):
    if index%2==1:
        content_text += content

for doc in set(docs):
    content_text = content_text.replace(doc,'')

for money_text in set(money_texts):
    content_text = content_text.replace(money_text,'')

for date in set(dates):
    content_text = content_text.replace(date, 'break_point')
    
content_text = content_text.replace('\n', ' ')

content_text = content_text.split('break_point')
content_text = [content.strip().replace('  ', ' ') for content in content_text]

print(f'Number of content: {len(content_text[1:])}')

#%% MERGE

df = pd.DataFrame({'date': dates,
                   'amount': moneys,
                   'content': content_text[1:]})

print(df.head())












        