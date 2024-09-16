#%% LIBRARY
import pdfplumber
import pandas as pd
pd.set_option('display.max_columns', None)

#%% EXTRACT DATA
file_path = 'data_original/sao_ke_MTTQ_VCB_13_9.pdf'

with pdfplumber.open(file_path) as pdf:
    pdf_length = len(pdf.pages)
    
def extract_pdf(file_path, start_page, end_page):
    with pdfplumber.open(file_path) as pdf:
        all_tables = []
        for page in pdf.pages[start_page:end_page]:
            box_table = (15, 10, 550, 830)
            # page.to_image().draw_rect(box_table).show()
            tables = page.within_bbox(box_table).extract_table()
            
            all_tables.extend(tables)
            
    return all_tables

start_page = 1
num_page = 400
pdf_length = 2

while start_page < pdf_length:
    end_page = min(pdf_length, start_page - 1 + num_page)
    data = extract_pdf(file_path, start_page - 1, end_page)
    
    if start_page == 1:
        data = data[1:]
    
    dates, moneys, contents = [], [], []
    for information in data:
        # extract date
        dates.append(information[1])
        
        # extract money
        moneys.append(information[2].replace('.', ''))
        
        # extract content
        contents.append(information[3].replace('\n', ' ').replace('"', ''))
        
    df = pd.DataFrame({
        'date': dates,
        'money': moneys,
        'content': contents
        })
    
    # df.to_csv('page_' + str(start_page) + '_' + str(end_page) + '.csv',
    #           index=False)
    
    # update start page
    start_page += num_page
