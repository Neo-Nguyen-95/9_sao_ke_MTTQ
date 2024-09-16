#%% LIBRARY
import re
import pdfplumber

#%% 0. EXTRACT DATA FROM PDF
def extract_pdf(file_path, start_page, end_page):
    with pdfplumber.open(file_path) as pdf:
        all_tables = []
        all_texts = ''
        for page in pdf.pages[start_page:end_page]:
            tables = page.extract_table()
            all_tables.extend(tables)
            
            all_texts += page.extract_text()
            
    return all_tables, all_texts

#%% I. EXTRACT DATE & DOCS
def table_to_date_doc(all_tables):

    dates, docs = [], []
    
    for index, content in enumerate(all_tables):
        if index % 2 == 1:
            dates.extend(content[0].splitlines()[0::2])
            docs.extend(content[0].splitlines()[1::2])
    
    return dates, docs

#%% II. EXTRACT MONEY & CONTENT
def clean_text(dates, docs, text):
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
    
    # split break point (add 1 space to distinguish from date in the content)
    pattern_2 = '|'.join(re.escape(date + ' ') for date in set(dates))
    content_text = re.sub(pattern_2, 'break_point', content_text)
    content_text = content_text.split('break_point')
    
    return [content.strip().replace('  ', ' ') for content in content_text if len(content)>1]

#%% VERIFICATION
def validation(dates, docs, content_text):
    if len(dates) == len(docs) and len(dates) == len(content_text):
        print(f'Number of transaction: {len(dates)}')
        print("Contents are valid")
    else:
        print("Contents are invalid")
        print(f'Number of date: {len(dates)}')
        print(f'Number of docs: {len(docs)}')
        print(f'Number of content: {len(content_text)}')