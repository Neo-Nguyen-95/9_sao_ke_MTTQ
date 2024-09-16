#%% LIBRARY
import os
import pandas as pd
import plotly.express as px
import numpy as np
import streamlit as st

# for spyder display
import plotly.io as pio
pio.renderers.default='browser'

def format_number(number):
    format_number = f"{number:,}"
    format_number = format_number.replace(',', '.')
    return format_number

#%% I. WRANGLE DATA
def merge_lv1(folder_path):
    file_list = os.listdir(folder_path)
    files = [folder_path + '/' + file for file in file_list if file != '.DS_Store']

    df = pd.DataFrame()
    for file in files:
        df_temp = pd.read_csv(file)
        df = pd.concat([df, df_temp], axis='rows')

    df['bank'] = folder_path.split('_')[1].lower()
    return df

def merge_lv2(folder_list):
    df = pd.DataFrame()
    for folder_path in folder_list:
        df_temp = merge_lv1(folder_path)
    
        df = pd.concat([df, df_temp], axis='rows')
    
    df = df.reset_index()
    df.drop(columns='index', inplace=True)
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
    
    return df

folder_list = ['data_VCB_1.9_10.9', 
                'data_Vietin_10.9_12.9', 
                'data_BIDV_1.9_12.9'
               ]
df = merge_lv2(folder_list)

#%% II. APP
st.set_page_config(
    page_title = 'THỐNG KÊ QUYÊN GÓP MẶT TRẬN TỔ QUỐC',
    page_icon = '💰',
    layout = 'wide'
    )

st.title('THỐNG KÊ QUYÊN GÓP MẶT TRẬN TỔ QUỐC')
st.markdown("""
            ## NGUỒN THÔNG TIN:
            Thông tin được tôi tổng hợp (cập nhật đến 15/09/2024) được lấy từ các
            tài liệu được Mặt Trận Tổ Quốc công bố tại link bên dưới:
         
            | STT | Tổ chức | Tài khoản | Ngày | Số lượt sao kê |
            |:-:|:-:|:-:|:-:|:-:|
            |1|[MTTQ - Ban cứu trợ trung ương](https://drive.google.com/file/d/18dIWiReYtJkyuQ_8vSBJWweGaD71rBpu/view)|VCB|1/9/2024-10/9/2024|200.364|
            |2|[MTTQ - Ban cứu trợ trung ương](https://drive.google.com/file/d/1ffkLOPymobFQjlklgpjabeHK7TX1ic3B/view)|Vietin|10/9/2024-12/9/2024|60.490|
            |3|[MTTQ - Ban cứu trợ trung ương](https://drive.google.com/file/d/15CcMvRMufl2v4_wtTD-qpL_lokjLo326/view)|BIDV|1/9/2024-12/9/2024|5.807|
            |4|[MTTQ - Ban cứu trợ trung ương](https://drive.google.com/file/d/14B6AeTF2QPAqx3jbzVoPaxGxteqV_h61/view)|VCB|11/9/2024|...(đang cập nhật)...|
            |5|[MTTQ - Ban cứu trợ trung ương](https://drive.google.com/file/d/145iywYGSaLCOwI4gqqW0dPPTTbz2v23i/view)|VCB|12/9/2024|...(đang cập nhật)...|
            """)   
#%% 2.1 EDA

st.markdown("""
            ## I. THỐNG KÊ
            """)

col_money, col_top10 = st.columns(2)
with col_money:
    total_money = format_number(df['money'].sum())
    
    st.write('Tổng số tiền từ các tài khoản quyên góp:')
    st.markdown(f"""
                <div style="background-color: #EDF4F2; border-radius: 10px; padding: 5px">
                <h1 style="font-size: 36px; color: #2F3C7E; text-align: center"> 
                {total_money} VND
                </h1>
                </div>
                """,
                unsafe_allow_html=True)
    
    total_donate_time = format_number(len(df))
    
    st.write('Tổng lượt quyên góp:')
    st.markdown(f"""
                <div style="background-color: #EDF4F2; border-radius: 10px; padding: 5px">
                <h1 style="font-size: 36px; color: #2F3C7E; text-align: center"> 
                {total_donate_time} lượt
                </h1>
                </div>
                """,
                unsafe_allow_html=True)
    
    st.write('Số tiền quyên góp giao động trong khoảng:')
    min_donate = format_number(df['money'].min())
    max_donate = format_number(df['money'].max())
    st.markdown(f"""
                <div style="background-color: #EDF4F2; border-radius: 10px; padding: 5px">
                <h1 style="font-size: 36px; color: #2F3C7E; text-align: center"> 
                Từ {min_donate} VND đến {max_donate} VND
                </h1>
                </div>
                """,
                unsafe_allow_html=True) 
    
with col_top10:
    st.write('Top 10 cá nhân/tập thể hảo tâm:')
    top_10_index = df['money'].sort_values(ascending=False)[:10].index
    df_top10 = df.iloc[top_10_index, 1:]
    df_top10 = df_top10.reset_index(drop=True)
    st.write(df_top10)
    
  

col_money_hist, col_donate_count = st.columns(2)
with col_money_hist:    
    
    money_array = np.array(df['money'])
    upper = np.quantile(money_array, 0.9)

    fig = px.histogram(df['money'][df['money'] < upper],
                        nbins=20
                        )
    fig.update_layout(xaxis_title='Số tiền [VND]',
                      yaxis_title='Số lượt',
                      title_text = 'Phân bố quyên góp',
                      showlegend=False)
    st.plotly_chart(fig)
    
    st.write('Biểu đồ thể hiện phân bố của 90% số tiền quyên góp, \
             10% còn lại quá lớn bạn đọc có thể xem trong bảng kê ở phần sau')
    
    
    
with col_donate_count:
  
    donate_count = df.groupby('date').count()
    
    fig = px.line(x=donate_count.index, y=donate_count['money'])
    fig.update_layout(
        xaxis=dict(
            tickformat="%d-%m"
            ),
        xaxis_title = 'Ngày quyên góp',
        yaxis_title = 'Số lượt quyên góp',
        title_text = 'Số lượt quyên góp mỗi ngày' ,
        )
    
    st.plotly_chart(fig)
    
    st.write('Biểu đồ thể hiện số lượt quyên góp qua từng ngày')

#%% 2.2 Search tool
st.markdown("""
            ## II. SAO KÊ CHI TIẾT
            """)

buff, col, buff2 = st.columns([1, 1, 1])
search_term = col.text_input("Nhập từ khóa tìm kiếm:")

buff, col, buff2 = st.columns([1, 4, 1])
if search_term:
    df_filter = df[df.apply(lambda row: search_term.lower() in row.to_string().lower(), 
                            axis='columns')]
    col.write("Dữ liệu lọc:")
    col.dataframe(df_filter)
else:
    col.write("Toàn bộ dữ liệu:")
    col.dataframe(df)

#%% DISCLAIMER
st.markdown("""
            ### Miễn trừ trách nhiệm: 
            Đây KHÔNG phải trang thông tin của một tổ chức có thẩm quyển mà là 
            sản phẩm của cá nhân, tôi KHÔNG đảm bảo tính chính xác hoàn toàn của 
            thông tin được đề cập. Các dữ liệu và phân tích trong ứng dụng này 
            được tôi tổng hợp và phân tích. Người sử dụng có trách nhiệm tự
            chịu rủi ro khi sử dụng thông tin được cung cấp trên ứng dụng này.
            Tôi tuyên bố miễn trừ hoàn toàn trách nhiệm đối với các lỗi hoặc 
            thiếu sót trong các thông tin. 
            """)

