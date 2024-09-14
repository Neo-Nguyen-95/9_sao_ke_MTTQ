#%% LIBRARY
import pdfplumber
import pandas as pd
import re
import time

pd.set_option('display.max_columns', None)

#%% LOAD DATA
file_path = 'data/sao_ke_MTTQ_full.pdf'

def extract_table(file_path):
    with pdfplumber.open(file_path) as pdf:
        all_tables = []
        all_texts = ''
        for page in pdf.pages[:1]:
            tables = page.extract_table()
            all_tables.extend(tables)
            
            all_texts += page.extract_text()
            
    return all_tables, all_texts

start_time = time.time()
all_tables, all_texts = extract_table(file_path)
end_time = time.time()
print(f"Elapsed time: {end_time - start_time}")

#%% I. EXTRACT DATE & DOCS
def table_to_date_doc(all_tables):

    dates, docs = [], []
    
    for index, content in enumerate(all_tables):
        if index % 2 == 1:
            dates.extend(content[0].splitlines()[0::2])
            docs.extend(content[0].splitlines()[1::2])
    
    return dates, docs

dates, docs = table_to_date_doc(all_tables)

# verification
if len(dates)==len(docs):
    print(f'Number of transaction: {len(dates)}')
    print("Dates and cash values are valid")
else:
    print('Conflict date and cash values')
    print(f'Number of date: {len(dates)}')
    print(f'Number of docs: {len(docs)}')

#%% II. EXTRACT MONEY & CONTENT
def clean_text(text):
    ### Split 1: Remove header and footer in the page
    text = re.sub(r'Số CT/ Doc No|Postal', 'break_point', text)  # detect break
    text = text.split('break_point')
    
    content_text = ''
    for index, content in enumerate(text):
        if index % 2 == 1:
            content_text += content
    
    ### Split 2: Separate content into pieces
    # remove docs and moneys infor from the text
    pattern_1 = '|'.join(re.escape(doc) for doc in set(docs))
            
    content_text = re.sub(pattern_1, '', content_text)
    
    # replace \n with space
    content_text = re.sub(r'\n', ' ', content_text)
    
    # split break point
    pattern_2 = '|'.join(re.escape(date) for date in set(dates))
    content_text = re.sub(pattern_2, 'break_point', content_text)
    content_text = content_text.split('break_point')
    
    return [content.strip().replace('  ', ' ') for content in content_text if len(content)>1]

content_text = clean_text(all_texts)

# verification
if len(dates) == len(content_text):
    print(f'Number of content: {len(content_text)}')
    print("Contents are valid")
else:
    print("Contents are invalid")

#%% MERGE
df = pd.DataFrame({'date': dates,
                   'full_content': content_text
                    })

df[['money', 'content']] = df['full_content'].str.split(' ', n=1, expand=True)
df['money'] = df['money'].str.replace('.', '', regex=False)

# df.to_csv('page_1_500.csv', index=False)
df.to_csv('test.csv', index=False)

end_time = time.time()
print(f"Total time: {end_time - start_time}")











        