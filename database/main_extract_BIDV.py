#%% LIBRARY
import pdfplumber
import pandas as pd

#%% EXTRACT DATA
file_path = 'data_original/sao_ke_MTTQ_BIDV_1.9_12.9.pdf'

with pdfplumber.open(file_path) as pdf:
    pdf_length = len(pdf.pages)

#%%
def extract_pdf(file_path, start_page, end_page):
    with pdfplumber.open(file_path) as pdf:
        all_tables = []
        for page in pdf.pages[start_page:end_page]:
            # test draw box
            box_table = (15, 10, 550, 830)
            # page.to_image().draw_rect(box_table).show()
            tables = page.within_bbox(box_table).extract_tables()
            
            for table in tables:
                all_tables.extend(table)
            
    return all_tables

start_page = 1
num_page = 500

while start_page < pdf_length:
    end_page = min(pdf_length, start_page - 1 + num_page)  # start page start at 1
    data = extract_pdf(file_path, start_page - 1, end_page)  # start page start at 1
    
    if start_page == 1:
        data = data[1:]
    
    index, dates, moneys, contents = [], [], [], []
    for information in data:
        # extract index
        # index.append(information[0])
        
        # extract date
        date_time = information[1].split(' ')
        date = date_time[0]
        dates.append(date)
        
        # extract money
        moneys.append(information[2].replace('.', ''))
        
        # extract content
        contents.append(information[3].replace('\n', ' '))
        
    df = pd.DataFrame({
        'index': index,
        'date': dates,
        'money': moneys,
        'content': contents
        })
    
    df.to_csv('page_' + str(start_page) + '_' + str(end_page) + '.csv',
              index=False)
    
    # update start page
    start_page += num_page
