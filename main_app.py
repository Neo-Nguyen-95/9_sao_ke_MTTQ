#%% I. LIBRARY & DATA
import pandas as pd
import plotly.express as px
import numpy as np
import streamlit as st
pd.set_option('display.max_columns', None)

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data_module import data_module

dataObject = data_module()
# dataObject.update_data()
df = dataObject.load_data()

# format function
def format_number(number):
    format_number = f"{int(number):,}"
    format_number = format_number.replace(',', '.')
    return format_number
#%% II. APP
st.set_page_config(
    page_title = 'THỐNG KÊ QUYÊN GÓP MẶT TRẬN TỔ QUỐC',
    page_icon = '💰',
    layout = 'wide'
    )

hide_menu_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.title('THỐNG KÊ QUYÊN GÓP KHẮC PHỤC HẬU QUẢ BÃO YAGI')

st.markdown("""
            ## I. METHODOLOGY
            
            """)

st.markdown("""
            ### Nguồn thông tin
            Thông tin được tôi tổng hợp (cập nhật đến 27/09/2024) được lấy từ các
            tài liệu được Mặt Trận Tổ Quốc công bố tại link các bên dưới:
         
            | STT | Tổ chức | Tài khoản | Ngày | Số lượt sao kê | Xác thực số liệu |
            |:-:|:-:|:-:|:-:|:-:|:-:|
            |1|[MTTQ - Ban cứu trợ trung ương](https://drive.google.com/file/d/18dIWiReYtJkyuQ_8vSBJWweGaD71rBpu/view)|VCB|1/9/2024-10/9/2024|200.364| Khớp số lượng |
            |2|[MTTQ - Ban cứu trợ trung ương](https://drive.google.com/file/d/14B6AeTF2QPAqx3jbzVoPaxGxteqV_h61/view)|VCB|11/9/2024|294.553| Khớp số lượng |
            |3|[MTTQ - Ban cứu trợ trung ương](https://drive.google.com/file/d/145iywYGSaLCOwI4gqqW0dPPTTbz2v23i/view)|VCB|12/9/2024|294.205| Khớp số lượng |
            |4|[MTTQ - Ban cứu trợ trung ương](https://drive.google.com/file/d/1vF8CZjFKEG2LsVjJgIiHZfsKLqu1h6ZM/view)|VCB|13/9/2024|386.402| Khớp số lượng |
            |5|[MTTQ - Ban cứu trợ trung ương](https://drive.google.com/file/d/1l03pejKXnjVXGj9RSnNVKQp5KVylfW-7/view)|VCB|14/9/2024|205.112| Khớp số lượng |
            |6|[MTTQ - Ban cứu trợ trung ương](https://www.mediafire.com/file/7r7budt2imc19hv/Thong_tin_ung_ho_qua_STK_VCB_0011001932418_tu_ngay_15.9_den_23.9.2024.pdf/file)|VCB|15/9/2024-23/9/2024|406.216| Khớp số lượng |
            |7|[MTTQ - Ban cứu trợ trung ương](https://drive.google.com/file/d/15CcMvRMufl2v4_wtTD-qpL_lokjLo326/view)|BIDV|1/9/2024-12/9/2024|5.807| Khớp số lượng |
            |8|[MTTQ - Ban cứu trợ trung ương](https://drive.google.com/file/d/1ffkLOPymobFQjlklgpjabeHK7TX1ic3B/view)|Vietin|10/9/2024-12/9/2024|60.490| Khớp số lượng |
            |9|[MTTQ - Ban cứu trợ trung ương](https://drive.google.com/file/d/119YkzrpkYAC4J3TYZYpvSX95yo-0OzP6/view)|Vietin|13/9/2024-15/9/2024|99.343| Khớp số lượng |
            |10|[MTTQ - Ban cứu trợ trung ương](https://www.mediafire.com/file/b7hjuv1f85zf6cc/Ng%25C3%25A0y_16.9.2024_T%25C3%25A0i_kho%25E1%25BA%25A3n_CT1111.pdf/file)|Vietin|16/9/2024|16.276|Khớp số lượng |
            |11|[MTTQ - Ban cứu trợ trung ương](https://www.mediafire.com/file/hp8fvor7a8ihtm7/Ng%25C3%25A0y_17.09.2024_T%25C3%25A0i_kho%25E1%25BA%25A3n_CT1111.pdf/file)|Vietin|17/9/2024|14.327|Khớp số lượng |
            |12|[MTTQ - Ban cứu trợ trung ương](https://www.mediafire.com/file/qsgvmdkqq78bup3/Ng%25C3%25A0y_18.09.2024_T%25C3%25A0i_kho%25E1%25BA%25A3n_CT1111.pdf/file)|Vietin|18/9/2024|7.534|Khớp số lượng |  
            |13|[MTTQ - Ban cứu trợ TP Hà Nội](https://drive.google.com/drive/u/0/folders/1LcwdlD34rJODyiosCTsFvF-bM6Rp23te)|Agribank|9/9/2024-12/9/2024|42.493| Khớp số tiền và số dư mỗi giao dịch |
            """)  

st.markdown("""
            ### Quy trình xử lí dữ liệu
            Để đảm bảo tính chính xác, tôi xử lí data theo mô hình bên dưới.
            """)

st.image('photos/method.jpg', caption='Methodology of data process')

st.markdown("""
            1. Thông tin được công bố trên mạng xã hội của Mặt Trận Tổ Quốc ở dạng 
            file PDF
            2. Data ở từng trang của file pdf được extract với pdfplumber
            3. Data được làm sạch và lưu trữ ở dạng bảng
            4. Kiểm tra tính chính xác của data bằng cách đối chiếu lại với số lượng
             giao dịch hoặc số dư sau mỗi giao dịch
            5. Lưu data sau khi làm sạch vào các file trong folder database
            6. Tổng hợp data vào một file theo format parquet để tăng tốc độ đọc file 
            7. Web app sẽ load trực tiếp file parquet để show số liệu bên dưới
            """)
#%% 2.1 EDA

st.markdown("""
            ## II. THỐNG KÊ 
            
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
    
    st.write('Tổng lượt quyên góp (đã loại trừ những khoản giao dịch 0 VND):')
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
    
    money_array = np.array(df['money'])
    quantile_25 = format_number(np.quantile(money_array, .25))
    quantile_75 = format_number(np.quantile(money_array, .75))
    median = format_number(np.quantile(money_array, .5))
    
    
    st.write('Trong đó:')
    st.markdown(f"""
                | 25% quantile | 50% quantile(median - trung vị) | 75% quantile| 
                |:-:|:-:|:-:|
                |{quantile_25}| {median}| {quantile_75}| 
                """)
    
with col_top10:
    st.write('Top 10 cá nhân/tập thể hảo tâm:')
    top_10_index = df['money'].sort_values(ascending=False)[:10].index
    df_top10 = df.iloc[top_10_index, 1:]
    df_top10 = df_top10.reset_index(drop=True)
    st.write(df_top10)
    
  

col_left, col_right = st.columns(2)
with col_left:    
    st.markdown("""
                **Histogram of distribution**
                """)
    option = st.selectbox('Chọn kiểu đồ thị phân bố:',
                 ['Giá trị thường', 'Giá trị log cơ số 10'], index=0)
    
    if option == 'Giá trị thường':
        money_array = np.array(df['money'])
        upper = np.quantile(money_array, 0.9)
    
        fig = px.histogram(df['money'][df['money'] < upper],
                            nbins=40
                            )
        fig.update_layout(xaxis_title='Số tiền [VND]',
                          yaxis_title='Số lượt',
                          title_text = 'Phân bố 90% quyên góp',
                          showlegend=False)
        st.plotly_chart(fig)
    
        st.write('Biểu đồ thể hiện phân bố của 90% số tiền quyên góp, \
             10% còn lại quá lớn bạn đọc có thể xem trong bảng kê ở phần sau')
    else:
        # log total donate histogram
        fig = px.histogram(np.log10(df['money']), nbins=80)
        fig.update_layout(xaxis_title='Log10(Số tiền) [VND]',
                          yaxis_title='Số lượt',
                          title_text = 'Phân bố toàn bộ quyên góp với giá trị Log10',
                          showlegend=False)
        st.plotly_chart(fig)
        st.write('Biểu đồ thể hiện phân bố của số tiền quyên góp qua giá trị log10')
    
with col_right:
    st.markdown("""
                **Line graph of mean values**
                """)
    st.write('')
    st.write('')
                
    option = st.checkbox('Show 25th & 75th quantile')
    
    # mean daily
    donate_mean = df['money'].groupby(df['date']).mean()
    donate_q25 = df['money'].groupby(df['date']).quantile(.25)
    donate_q75 = df['money'].groupby(df['date']).quantile(.75)
    
    fig = px.line(x=donate_mean.index, y=donate_mean.values, markers=True)
    
    if option:
        fig.add_trace(go.Scatter(
            x=donate_mean.index, y=donate_q25,
            mode='lines',
            name='Line of 25th quantile',
            line=dict(color='#f5b7b1')
            ))
        
        fig.add_trace(go.Scatter(
            x=donate_mean.index, y=donate_q75,
            mode='lines',
            name='Line of 75th quantile',
            line=dict(color='#f5b7b1'),
            fill='tonexty', fillcolor='rgba(255, 0, 0, 0.1)'
            ))
    
    fig.update_layout(
        xaxis=dict(tickformat="%d-%m"),
        xaxis_title='Ngày',
        yaxis_title='Số tiền trung bình/lần [VND]',
        title_text = 'Số tiền quyên góp trung bình mỗi ngày',
        showlegend=False,
        )
    
    st.plotly_chart(fig)
    st.markdown("""
                Đường màu xanh thể hiện giá trị trung bình mỗi ngày, còn \
                giá trị quantile 25% và 75% được thể hiện qua dải màu đỏ.
                """)
    
# donate each day
donate_count = df.groupby('date').count()
donate_amount = df['money'].groupby(df['date']).sum()

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Scatter(
    x=donate_count.index, y=donate_count['money'],
    line=dict(color='#6495ED'),
    mode='lines+markers', name='Số lượt quyên góp'
    ), secondary_y=False)

fig.add_trace(go.Scatter(
    x=donate_amount.index, y=donate_amount.values, 
    line=dict(color='#2ecc71'),
    mode='lines+markers', name='Số tiền quyên góp'
    ), secondary_y=True)

fig.update_layout(
    xaxis=dict(
        tickformat="%d-%m",
        title='Ngày quyên góp'
        ),
    yaxis=dict(
        gridcolor='#d6eaf8'),
    yaxis2=dict(
        gridcolor='#d4efdf'),
    title_text = 'Thống kê quyên góp mỗi ngày',
    )

fig.update_yaxes(title_text="Số lượt quyên góp", 
                 secondary_y=False)
fig.update_yaxes(title_text="Số tiền quyên góp", 
                 secondary_y=True)


st.plotly_chart(fig)

st.write('Biểu đồ thể hiện số lượt quyên góp qua từng ngày')

#%% 2.2 Search tool
st.markdown("""
            ## III. SAO KÊ CHI TIẾT
            """)

col, buff, buff2 = st.columns([1, 1, 1])
search_term = col.text_input("Nhập từ khóa tìm kiếm:")

if search_term:
    df_filter = df[df['content'].str.contains(search_term, case=False)]
    st.write("Dữ liệu lọc:")
    st.dataframe(df_filter, width=1200)
else:
    st.write("Dữ liệu sao kê mẫu:")
    df_show = df.head(10)
    st.dataframe(df_show, width=1200)

#%% DISCLAIMER
st.markdown("""
            <div style="text-align: center">
            
            
            ___
            
            
            </div>
            """,
            unsafe_allow_html=True)

col1, buff, col2 = st.columns([2, .5, 7])
col1.markdown("""
              ### About me:
              Hi there! I am Neo, a data enthusiast. It is great if you are intested in my work.
              Meet me at [Facebook](https://www.facebook.com/lun.cao), [LinkedIn](https://www.linkedin.com/in/viet-dung-nguyen-87809311a/)
              """)
col2.markdown("""
            ### Miễn trừ trách nhiệm: 
            Đây KHÔNG phải trang thông tin của một tổ chức có thẩm quyển mà là 
            sản phẩm của cá nhân, tôi KHÔNG đảm bảo tính chính xác hoàn toàn của 
            thông tin được đề cập. Các dữ liệu và phân tích trong ứng dụng này 
            được tôi tổng hợp và phân tích. Người sử dụng có trách nhiệm tự
            chịu rủi ro khi sử dụng thông tin được cung cấp trên ứng dụng này.
            Tôi tuyên bố miễn trừ hoàn toàn trách nhiệm đối với các lỗi hoặc 
            thiếu sót trong các thông tin. 
            """)

