import numpy as np
import pandas as pd
import random
import streamlit as st
    
st.set_page_config(layout="wide")

st.title('口コミのトピック分類')

def create_csv():
    df_review_random_normal.to_csv(f'test_data_streamlit/{target_product}_{ver}.csv', index_col=0)
    df_review_random = df_review_random_normal
    

with st.form("version_form"):
    target_product = st.selectbox(
            "入力する製品を選んでください",
            ['皮脂テカリ防止下地_450','保湿力スキンケア下地_450','マットシフォン UVホワイトニングベースN_450']
        )
    
    ver = st.text_input("バージョンを入力してください")
   
    st.form_submit_button('更新', on_click=create_csv)

df_review_random_normal = pd.read_csv(f'test_data_streamlit/{target_product}.csv', index_col=0)

random_list = list(pd.read_csv('test_data_streamlit/random_list.csv',index_col=0)['0'])
    

st.write('現在のバージョン：', ver)
col1, col2 = st.columns([2, 1], gap='large')

try:
    df_review_random = pd.read_csv(f'test_data_streamlit/{target_product}_{ver}.csv', index_col=0)
except FileNotFoundError:
    col1.warning('バージョンを入力してください')


with col2:
    st.subheader("選択項目")
    df_topic = pd.read_csv('test_data_streamlit/トピックリスト.csv',index_col=0)
    
    with st.form("topic_form", clear_on_submit=False): 
        submitted = st.form_submit_button("Submit")
        
        count = st.number_input("番号を入力してください", min_value=0, max_value=34, value="min") 

                  
        options = st.multiselect(
            "トピックを選択してください",
            list(df_topic['トピック'])
        ) 
        
        if submitted:
            st.write("選ばれたトピック:", list(options))
                                                                                                                                                                                                                                                            

    if submitted:
        if count != None:
            df_review_random.at[count, 'トピック'] = str(options)
            df_review_random.to_csv(f'test_data_streamlit/{target_product}_{ver}.csv')
        
    
    
with col1:
    st.subheader("口コミ本文")
    
    if count != None:
        idx = random_list[count+1]
        
        review = df_review_random.loc[count+1,'本文']
        st.write(f'{count+1}.レビュー番号{idx}:\n\n{review}')
    
    st.table(df_review_random)

        

