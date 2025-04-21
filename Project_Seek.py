import pandas as pd
import requests
import time

# ✅ 사용자 설정
API_KEY = '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'
CX = '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'
INPUT_FILE = r"C:\Users\DeokHwangbo\Downloads\Hope.xlsx"
OUTPUT_FILE = r"C:\Users\DeokHwangbo\Downloads\Result.xlsx"

# 📥 엑셀 파일에서 IMEI 목록 불러오기
df = pd.read_excel(INPUT_FILE)
imei_list = df['IMEI'].astype(str).tolist()  # 'IMEI' 열 이름이 다르면 수정

# 📤 결과 저장용 리스트
results_all = []

# 🔍 Google 검색 함수
def search_imei(imei):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CX,
        "q": imei,
        "num": 3  # 결과 개수 조정 가능
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get("items", [])

# 🚀 IMEI별 검색 실행
for imei in imei_list:
    print(f"Searching: {imei}")
    try:
        items = search_imei(imei)
        if items:
            for item in items:
                results_all.append({
                    'IMEI': imei,
                    'Title': item.get('title'),
                    'Link': item.get('link'),
                    'Snippet': item.get('snippet')
                })
        else:
            results_all.append({
                'IMEI': imei,
                'Title': 'No result',
                'Link': '',
                'Snippet': ''
            })
        time.sleep(1)  # Google API rate limit 대비
    except Exception as e:
        results_all.append({
            'IMEI': imei,
            'Title': f'Error: {e}',
            'Link': '',
            'Snippet': ''
        })

# 📤 결과를 엑셀 파일로 저장
output_df = pd.DataFrame(results_all)
output_df.to_excel(OUTPUT_FILE, index=False)
print(f"\n✅ 결과 저장 완료: {OUTPUT_FILE}")