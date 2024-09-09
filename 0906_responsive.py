import numpy as np
import pandas as pd
import random
import streamlit as st
    
st.set_page_config(layout="wide")

option_device = st.selectbox(
    "どちらのモードで表示しますか？",
    ("パソコン", "スマートフォン"),
)
    
st.title('口コミのトピック分類')

def create_csv():
    st.session_state["df_review_random"] = df_review_random_normal
    
def uploaded_csv():
    # ファイルがアップロードされたか確認
    if uploaded_file is not None:
        # pandasで読み込む
        try:
            st.session_state["df_review_random"] = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"ファイルの読み込み中にエラーが発生しました: {e}")   
        
        
with st.form("version_form"):
    target_product = st.selectbox(
            "入力する製品を選んでください",
            ['皮脂テカリ防止下地_450','保湿力スキンケア下地_450','マットシフォン UVホワイトニングベースN_450']
        )
    df_review_random_normal = pd.read_csv(f'./test_data_streamlit/{target_product}.csv', index_col=0)
    
    ver = st.text_input("バージョンを入力してください")
   
    btn_version = st.form_submit_button('新規作成', on_click=create_csv)


# with st.expander("続きから作成する"):
with st.form("続きから作成する"):
    uploaded_file = st.file_uploader("fileを追加してください")
    btn_uploaded = st.form_submit_button('続きから作成', on_click=uploaded_csv)
    
random_list = list(pd.read_csv(f'./test_data_streamlit/random_list.csv',index_col=0)['0'])
    
if ver =="" and uploaded_file is None:
    st.warning('バージョンを入力するか、ファイルをアップロードしてください')
    

df_topic = pd.read_csv(f'./test_data_streamlit/トピックリスト.csv',index_col=0)

def create_right_col():
    st.subheader("選択項目")
        
    with st.form("topic_form", clear_on_submit=False):        
        st.session_state["count"] = st.number_input("番号を合わせてください", min_value=-1, max_value=34, value="min") 

                  
        options = st.multiselect(
            "トピックを選択してください",
            list(df_topic['トピック'])
        ) 
        
        submitted = st.form_submit_button("Submit")
    
                                                                                                                                                                                                                                                            

    if submitted:
        st.session_state["df_review_random"].at[st.session_state["count"], 'トピック'] = str(options)
        st.session_state["df_review_random"].to_csv(f'./test_data_streamlit/{target_product}_{ver}.csv')
    
    @st.cache_data
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode("utf-8")

    csv = convert_df(st.session_state["df_review_random"])

    if ver !="" or uploaded_file is not None:
        btn_save_csv = st.download_button(
            label="入力したデータを保存する",
            data=csv,
            file_name=f'{target_product}_{ver}.csv',
            mime="text/csv",
        )
        
        
def create_left_col():
    st.subheader("口コミ本文")
    
    # try:
    if ver !="" or uploaded_file is not None:
        idx = random_list[st.session_state["count"]+1]
        review = st.session_state["df_review_random"].loc[st.session_state["count"]+1,'本文']
        st.write(f'{st.session_state["count"]+1}.レビュー番号{idx}:\n\n{review}')
        st.table(st.session_state["df_review_random"])


if option_device == "スマートフォン":
    create_right_col()
    create_left_col()
    
else:
    col1, col2 = st.columns([2, 1], gap='large')
    with col2:
        create_right_col()
    with col1:
        create_left_col()