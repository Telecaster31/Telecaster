import streamlit as st
import pandas as pd
import re
from io import BytesIO

# 이미지 URL 설정
initial_image_url = "https://mblogthumb-phinf.pstatic.net/MjAyMjA1MjNfNDgg/MDAxNjUzMjMzMjQwMzc3.XZDjgEUamZdHHJti0EwSn2l9nTveii3Hy_GIG50qZhAg.NZGNIKs6eFU_4aprDKbtjveO1oosVy0EpGh_aZgDgWwg.PNG.gummy27131/%EC%A6%90%EA%B2%81%EB%8B%A4.png?type=w800"
success_image_url = "https://mblogthumb-phinf.pstatic.net/MjAyMjA1MjNfMTQx/MDAxNjUzMjMzMjQwMzc5.g9-1_bp8xbOR1rEMPxIGYU-WwmOlLewMkESXkUtj5oUg.YWptYzAKEWOzR1tiqfjUguttGBPWcCz7e_zUasgXdaog.PNG.gummy27131/%EB%A7%88%EC%B0%B8%EB%82%B4.png?type=w800"  # ✅ 작업 완료 후 표시할 이미지

# 파일 업로드 전에는 초기 이미지 보여줌
if "filter_done" not in st.session_state:
    st.session_state.filter_done = False

# 작업 성공 여부에 따라 이미지 다르게 표시
if st.session_state.filter_done:
    st.image(success_image_url, width=100)
else:
    st.image(initial_image_url, width=200)

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

    # 작업 성공 이미지 표시
    st.session_state.filter_done = True
    st.success("✅ 필터링 완료! 아래에서 다운로드 하세요.")
    st.dataframe(df)

    @st.cache_data
    def convert_df_to_xlsx(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Filtered Data')
        return output.getvalue()

    xlsx_data = convert_df_to_xlsx(df)

    st.download_button(
        label="📥 엑셀 다운로드 (xlsx)",
        data=xlsx_data,
        file_name="WMS_Filtered_Result.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )