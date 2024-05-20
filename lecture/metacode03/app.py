# app.py 파일을 만들어라, 셀의 내용이 들어간
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 데이터 로드
# @ 데코레이터 함수
@st.cashe_data
def load_data():
    olist = pd.read_csv('./dataset/List of Orders.csv')
    detail = pd.read_csv('./dataset/Order Details.csv')
    data = olist.merge(detail, on = 'Order ID')

    return data
# 차트를 그릴 때마다 데이터를 새로 불러와야하는 문제를 해결
# 캐시메모리에 load_data() 결과를 저장해놓고, 필요할 떄 여기서부터 시작함

def preproc():
    data['Order Date'] = pd.to_datetime(data['Order Date'], format = '%d-%m-%Y')
    data['year']      = data['Order Date'].dt.year
    data['month']     = data['Order Date'].dt.month
    data['yearmonth'] = data['Order Date'].astype('str').str.slice(0,7)

    return data

def line_chart(data, x, y, title):
    df = data.groupby(x).agg({y : 'sum'}).reset_index()
    fig = px.line(df, x=x, y=y, title=title)
    fig.show()

    return fig

def bar_chart(data, x, y, color=None):
    if color is not None:
        index = [x, color]
    else :
        index = x
    
    df = data.pivot_table(index = index, values = y, aggfunc = 'sum').reset_index()
    fig = px.bar(df, x=x, y=y, color = color)
    fig.show()

    return fig

def heat_map(data, z, title):
    #df = data.pivot_table(index=['State', 'Sub-Category'], values=['Quantity', 'Amount', 'Profit']).reset_index()
    df = data.pivot_table(index=['State', 'Sub-Category'], values=['Quantity', 'Amount']).reset_index()
    fig = px.density_heatmap(df, x='State', y='Sub-Category', z=z, title=title)
    fig.show()
    return fig


if __name__ == '__main__':

    st.title([)'E-Commerce Data 분석')
    st.write('시각화 대시보드 만들기')

    #데이터 로드
    data = load_data()
    # 데이터 전처리
    data = preproc()

st.subheader('월별 판매량 분석')
with st.form('form', clear_on_submit = True):
    col1, col2 = st.columns(2)
    submitted1 = col1.form_submit_button('판매량 그래프')
    submitted2 = col2.form_submit_button('매출액 그래프')

    if submitted1:
        df1, fig1 = line_chart(data, 'yearmonth', 'Quantity', 'Sales Quantity by month')
        st.dataframe(df1.T)
        dt.plotly_chart(fig1, theme="streamlit", use_container_width=True)
    elif submitted2:
        df2, fig2 = line_chart(data, 'yearmonth', 'Amount', 'Sales Quantity by month')
        st.dataframe(df2.T)
        st.plotly_chart(fig2, theme='streamlit', use_container_width=True)


st.subheader('품목별 판매량')
col1, col2 = st.columns(2)
with col1:
    col1.subheader('카테고리별 판매량')
    fig3 = bar_chart(data, 'Category', 'Quantity')
    st.plotly_chart(fig3, theme='streamlit',use_container_width=True)

with col2:
    col2.subheader('월별/카테고리별 누적 차트')
    fig4 = bar_chart(data, 'yearmonth', 'Quantity','Category')
    st.plotly_chart(fig4, theme='streamlit',use_container_width=True)


st.subheader('지역별 주력 판매상품')
tab1, tab2 = st.tabs(['Quantity heat map', 'Amount heat map'])
with tab1:
    fig5 = heatmap(data, 'Quantity', 'Quantity heat map')
    st.plotly_chart(fig5, theme='streamlit',use_container_width=True)

with tab2:
    fig6 = heatmap(data, 'Amount', 'Amount heat map')
    st.plotly_chart(fig6, theme='streamlit',use_container_width=True)


    
