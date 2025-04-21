import streamlit as st
import pandas as pd
import re
from io import BytesIO

# 이미지 설정
initial_image_url = "https://mblogthumb-phinf.pstatic.net/MjAyMjA1MjNfNDgg/MDAxNjUzMjMzMjQwMzc3.XZDjgEUamZdHHJti0EwSn2l9nTveii3Hy_GIG50qZhAg.NZGNIKs6eFU_4aprDKbtjveO1oosVy0EpGh_aZgDgWwg.PNG.gummy27131/%EC%A6%90%EA%B2%81%EB%8B%A4.png?type=w800"
success_image_url = "https://mblogthumb-phinf.pstatic.net/MjAyMjA1MjNfMTQx/MDAxNjUzMjMzMjQwMzc5.g9-1_bp8xbOR1rEMPxIGYU-WwmOlLewMkESXkUtj5oUg.YWptYzAKEWOzR1tiqfjUguttGBPWcCz7e_zUasgXdaog.PNG.gummy27131/%EB%A7%88%EC%B0%B8%EB%82%B4.png?type=w800"

# 상태 초기화
if "filter_done" not in st.session_state:
    st.session_state.filter_done = False
if "filtered_df" not in st.session_state:
    st.session_state.filtered_df = None

# 이미지 출력
st.image(success_image_url if st.session_state.filter_done else initial_image_url, width=300)
st.title("📂 마감 자료 자동화")

uploaded_file = st.file_uploader("WMS 엑셀 파일을 업로드해주세요", type=["xlsx"])

# 최초 업로드 시 필터 처리
if uploaded_file and not st.session_state.filter_done:
    try:
        df = pd.read_excel(uploaded_file)

        if df.empty:
            st.error("❌ 업로드된 파일에 유효한 데이터가 없습니다.")
            st.stop()

        columns_to_keep = [
            'SPO Ref. 1', 'Contact', 'Tel', 'Address Line 1',
            'ASN Ref. No.', 'Item No.', 'Item Description',
            'Type of Order', 'Transport Time'
        ]

        missing_columns = [col for col in columns_to_keep if col not in df.columns]
        if missing_columns:
            st.warning(f"❗ 다음 컬럼이 누락되어 있어 제외되었습니다: {missing_columns}")

        df = df[[col for col in columns_to_keep if col in df.columns]]

        if 'Item Description' in df.columns:
            df = df[~df['Item Description'].astype(str).str.contains('bolttech', case=False, na=False)]

        if 'SPO Ref. 1' in df.columns:
            df = df[df['SPO Ref. 1'].astype(str).str.match(r'^1\d{14}$')]

        # ✅ 안전하게 저장
        st.session_state.filtered_df = df
        st.session_state.filter_done = True
        st.rerun()

    except Exception as e:
        st.error(f"❌ 처리 중 오류 발생: {e}")
        st.stop()

# 결과 출력
if st.session_state.filter_done and st.session_state.filtered_df is not None:
    df = st.session_state.filtered_df
    st.success("✅ 필터링 완료! 아래에서 다운로드 하세요.")
    st.dataframe(df)

    @st.cache_data
    def convert_df_to_xlsx(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Filtered Data")
        return output.getvalue()

    xlsx_data = convert_df_to_xlsx(df)

    st.download_button(
        label="📥 엑셀 다운로드 (xlsx)",
        data=xlsx_data,
        file_name="WMS_Filtered_Result.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )