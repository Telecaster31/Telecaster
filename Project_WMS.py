import streamlit as st
import pandas as pd
import re

st.title("📂 WMS 엑셀 필터링 툴")

uploaded_file = st.file_uploader("WMS 엑셀 파일을 업로드해주세요", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # 필드 필터링
    columns_to_keep = [
        'SPO Ref. 1', 'Contact', 'Tel', 'Address Line 1',
        'ASN Ref. No.', 'Item No.', 'Item Description',
        'Type of Order', 'Transport Time'
    ]
    df = df[columns_to_keep]

    # 'bolttech' 포함 행 제거
    df = df[~df['Item Description'].astype(str).str.contains('bolttech', case=False, na=False)]

    # '1'로 시작하는 15자리 SPO Ref. 1만 남기기
    pattern = r'^1\d{14}$'
    df = df[df['SPO Ref. 1'].astype(str).str.match(pattern)]

    st.success("✅ 필터링 완료! 아래에서 다운로드 하세요.")
    st.dataframe(df)

    # 다운로드
    @st.cache_data
    def convert_df(df):
        return df.to_excel(index=False, engine='openpyxl')

    st.download_button(
        label="📥 엑셀 다운로드",
        data=convert_df(df),
        file_name="WMS_Filtered_Result.xlsx"
    )