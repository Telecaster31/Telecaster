# SMS 자동 작성 코드

import pandas as pd

# Load the Excel file
file_path = r"C:\Users\DeokHwangbo\Downloads\강제해지SMS\(블랙리스트)강제해지LIST.xlsx"
df = pd.read_excel(file_path, dtype={'change_date1': str, 'change_date2': str, 'change_date3': str, 'change_date4': str, 'cancel_subscription_date': str})

# Fill NaN values with empty strings
df = df.fillna('')

# Define the template text
template = """[LG U+ 폰교체 서비스]

{고객명} 고객님 안녕하세요, 폰교체 서비스 고객센터입니다.

당사는 이용약관 제3조 제4항을 통해 가입 신청자가 마지막 교체휴대폰을 수령한 날을 기준으로
직전 1년 간 해당 명의자가 보유한 전체 회선에서 폰교체 서비스를 통해 교체한 횟수가 4회 이상이거나
미반납 교체가 2회 이상인 경우, 전체 회선에서 이루어진 마지막 교체일로부터 24개월동안 서비스 가입이
제한됨을 밝히고 있습니다.

고객님께서 {해지구독일자}에 {해지구독회선} 회선으로 본 서비스에 가입 신청하셨을 때는 
{교체정보}, 1년 간 총 {N}회의 교체 이력이 확인되므로 가입이 제한되었어야 합니다.

따라서 당사는 귀하의 {해지구독회선} 회선에 대한 폰교체패스 구독을 해지하고 이미 납부하신 월이용료를
환불해 드리겠습니다.

감사합니다.
볼트테크코리아 주식회사 드림.
"""

# Initialize an empty string to hold all cases
all_cases_text = ""

# Function to format date to year-month-day
def format_date(date_str):
    if pd.isna(date_str) or not isinstance(date_str, str) or date_str.strip() == "":
        return ""
    try:
        return pd.to_datetime(date_str, errors='coerce').strftime('%Y년 %m월 %d일')
    except ValueError:
        return ""

# Iterate through the dataframe and generate the text for each case
for index, row in df.iterrows():
    # Collect change information
    changes = []
    for i in range(1, 5):
        date_col = f'change_date{i}'
        type_col = f'change_type{i}'
        if pd.notna(row[date_col]) and pd.notna(row[type_col]):
            formatted_date = format_date(row[date_col])
            if formatted_date:
                changes.append(f"{formatted_date} {row[type_col]}")

    # Join changes into a string
    교체정보 = ', '.join(changes)

    # Fill the template with the adjusted row data
    case_text = template.format(
        고객명=row['customer_name'],
        해지구독회선=row['cancel_subscription_line'],
        해지구독일자=format_date(row['cancel_subscription_date']),
        교체정보=교체정보,
        N=row['total_changes']
    )
    
    # Append the case text to the all cases text
    all_cases_text += case_text + "\n\n"

# Define the output file path
output_file_path = r"C:\Users\DeokHwangbo\Downloads\강제해지SMS\2025.04.21_블랙리스트LIST.txt"

# Write the combined text to the file
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(all_cases_text)

print(f"텍스트 파일 작성완료!: {output_file_path}")