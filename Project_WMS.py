import streamlit as st
import pandas as pd
import re
from io import BytesIO

st.image("https://mblogthumb-phinf.pstatic.net/MjAyMjA1MjNfNDgg/MDAxNjUzMjMzMjQwMzc3.XZDjgEUamZdHHJti0EwSn2l9nTveii3Hy_GIG50qZhAg.NZGNIKs6eFU_4aprDKbtjveO1oosVy0EpGh_aZgDgWwg.PNG.gummy27131/%EC%A6%90%EA%B2%81%EB%8B%A4.png?type=w800", width=200)
st.title("📂 마감 자료 자동화")

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

    # 엑셀 파일 변환
    @st.cache_data
    def convert_df_to_xlsx(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Filtered Data')
        return output.getvalue()

    xlsx_data = convert_df_to_xlsx(df)

    # 다운로드 버튼
    st.download_button(
        label="📥 엑셀 다운로드 (xlsx)",
        data=xlsx_data,
        file_name="WMS_Filtered_Result.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
