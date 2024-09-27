#%% LIBRARY
import pdfplumber
import pandas as pd
pd.set_option('display.max_columns', None)

#%% EXTRACT DATA
file_path = 'data_original/sao_ke_MTTQ_VCB_15.9_23.9.pdf'

with pdfplumber.open(file_path) as pdf:
    pdf_length = len(pdf.pages)
    
def extract_pdf(file_path, start_page, end_page):
    with pdfplumber.open(file_path) as pdf:
        all_tables = []
        for page in pdf.pages[start_page:end_page]:
            # box_table = (15, 10, 550, 830)
            # page.to_image().draw_rect(box_table).show()
            tables = page.extract_table()
            
            all_tables.extend(tables)
            
    return all_tables

# pdf_length = 2
start_page = 1
num_page = 400

while start_page < pdf_length:
    end_page = min(pdf_length, start_page - 1 + num_page)
    data = extract_pdf(file_path, start_page - 1, end_page)
    
    if start_page == 1:
        data = data[2:]
    
    df = pd.DataFrame(data, columns=['index', 'date', 'money', 'buff1', 'content'])
    
    df['date'] = df['date'].str.split(' ', expand=True)[0]
    df['money'] = df['money'].str.replace('.','').str.split(',', expand=True)[0]
    df['content'] = df['content'].str.replace('\n',' ')
    df.drop(columns=['index', 'buff1'], inplace=True)
    
    df.to_csv('page_' + str(start_page) + '_' + str(end_page) + '.csv',
              index=False)
    
    # update start page
    start_page += num_page
