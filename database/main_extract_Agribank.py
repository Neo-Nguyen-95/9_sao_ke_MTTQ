#%% LIBRARY
import pdfplumber
import pandas as pd
pd.set_option('display.max_columns', None)

#%% EXTRACT DATA
file_path = 'data_original/sao_ke_MTTQ HN_9.9_12.9.pdf'

with pdfplumber.open(file_path) as pdf:
    pdf_length = len(pdf.pages)
    
def extract_pdf(file_path, start_page, end_page):
    with pdfplumber.open(file_path) as pdf:
        all_tables = []
        for page in pdf.pages[start_page:end_page]:
            # box_table = (15, 10, 550, 830)
            # page.to_image().draw_rect(box_table).show()
            # tables = page.within_bbox(box_table).extract_table()
            tables = page.extract_table()
            
            all_tables.extend(tables)
            
    return all_tables

# pdf_length = 2
start_page = 1706
start_name = start_page
num_page = 1

df = pd.DataFrame()
while start_page <= pdf_length:
    end_page = min(pdf_length, start_page - 1 + num_page)
    data = extract_pdf(file_path, start_page - 1, end_page)        
    
    dates, moneys, contents, balance = [], [], [], []
    for information in data:
        
        try:
            if int(information[3].replace(',','')):
                # extract date
                dates.append(information[0])
                
                # extract money
                moneys.append(information[3].split(' ')[-1].replace(',',''))
                
                # extract content
                contents.append(information[1].replace('\n', ' '))
                
                # extract balance
                balance.append(information[4].replace(',',''))
        except:
            pass
    df_temp = pd.DataFrame({
        'date': dates,
        'money': moneys,
        'content': contents,
        'balance': balance
        })
    
    
    # check
    try:
        print(f'Now at page {end_page}')
        if df_temp['money'][1:].astype(int).sum() == (
                df_temp['balance'].astype(int).iloc[-1] - df_temp['balance'].astype(int).iloc[0]):
            df = pd.concat([df, df_temp], axis='rows')
            
            if end_page%200 == 0:
                df.to_csv('page_' + str(start_name) + '_' + str(end_page) + '.csv',
                          index=False)
            
            # update start page
            start_page += num_page
        else:
            df.to_csv('page_' + str(start_name) + '_' + str(end_page-1) + '.csv',
                      index=False)
            break
    except:
        df.to_csv('page_' + str(start_name) + '_' + str(end_page-1) + '.csv',
                  index=False)
        print(f'Stop at: {end_page}')
        start_page = pdf_length + 1
        break
    
pd.DataFrame(data).to_csv('page_' + str(end_page) + '.csv', index=False)  


