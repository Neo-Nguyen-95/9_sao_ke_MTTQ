#%% LIBRARY
import pandas as pd
import pdfplumber
from VCB_extraction import extract_pdf, table_to_date_doc, clean_text, validation

pd.set_option('display.max_columns', None)

file_path = 'data_original/sao_ke_MTTQ_VCB_1.9_10.9.pdf'
#%% COUNT NUMBER OF PAGE

with pdfplumber.open(file_path) as pdf:
    pdf_length = len(pdf.pages)

#%% DATA MINING
def pdf_mining(file_path, start_page, num_page):
    # condider it reach the final page
    end_page = min(pdf_length, start_page - 1 + num_page)
    all_tables, all_texts = extract_pdf(file_path, start_page - 1, end_page)

    dates, docs = table_to_date_doc(all_tables)
    
    content_text = clean_text(dates, docs, all_texts)
    
    validation(dates, docs, content_text)

    # merge
    df = pd.DataFrame({'date': dates,
                       'full_content': content_text
                        })
    # data wrangle
    df[['money', 'content']] = df['full_content'].str.split(' ', n=1, expand=True)
    df.drop(columns='full_content', inplace=True)
    df['money'] = df['money'].str.replace('.', '', regex=False)
    
    # df.to_csv('page_1_500.csv', index=False)
    df.to_csv('page_' + str(start_page) + '_' + str(end_page) + '.csv', 
              index=False)
    
    return df

start_page = 1
while start_page < pdf_length:
    num_page = 400
    df = pdf_mining(file_path, start_page, num_page)
    # update start_page
    start_page += num_page









        