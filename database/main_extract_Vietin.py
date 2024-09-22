#%% LIBRARY
import pdfplumber
import pandas as pd

#%% EXTRACT DATA
file_path = 'data_original/sao_ke_MTTQ_Vietin_13.9_15.9.pdf'

with pdfplumber.open(file_path) as pdf:
    pdf_length = len(pdf.pages)
    
def extract_pdf(file_path, start_page, end_page):
    with pdfplumber.open(file_path) as pdf:
        all_tables = []
        for page in pdf.pages[start_page:end_page]:
            tables = page.extract_table()
            all_tables.extend(tables)
            
    return all_tables

start_page = 1
num_page = 400

while start_page < pdf_length:
    end_page = min(pdf_length, start_page - 1 + num_page)
    data = extract_pdf(file_path, start_page - 1, end_page)
    
    if start_page == 1:
        data = data[1:]
    
    dates, moneys, contents = [], [], []
    for information in data:
        # extract date
        date_time = information[1].split('\n')
        date = date_time[0]
        dates.append(date)
        
        # extract money
        moneys.append(information[3].replace('.', ''))
        
        # extract content
        contents.append(information[2].replace('\n', ' '))
        
    df = pd.DataFrame({
        'date': dates,
        'money': moneys,
        'content': contents
        })
    
    df.to_csv('page_' + str(start_page) + '_' + str(end_page) + '.csv',
              index=False)
    
    # update start page
    start_page += num_page

