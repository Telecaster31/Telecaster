# SMS 자동 작성 코드

import pandas as pd

# Load the Excel file
file_path = r"C:\Users\DeokHwangbo\Downloads\py\Project_BT\Plastics\BYE.xlsx"
df = pd.read_excel(file_path, dtype={'구독개시일': str, '교체신청일': str})

# Fill NaN values with empty strings
df = df.fillna('')

# Define the template text
template = """[LG U+ 폰교체 서비스]

{고객명} 고객님 안녕하세요 폰교체 서비스 고객센터입니다.

당사는 서비스 이용약관 제14조 제4항을 통해 서비스 오남용 행위가 확인된 경우,
신청한 교체 휴대폰 제공을 거부하고 서비스를 즉시 해지할 수 있음을 밝히고 있습니다.

당사의 조사 결과, 귀하께서 {구독개시일}에 {가입회선}으로 본 서비스에 가입하신 후
{교체신청일}에 신청하신 미반납교체가 서비스 오남용 행위인 것으로 판단되었습니다.

따라서 당사는 이용약관에 따라 귀하께서 유지 중인 서비스 구독을 해지하기로 하였으며,
구독이 해지됨에 따라 신청하신 교체 휴대폰은 제공해드릴 수 없습니다.

감사합니다.
볼트테크코리아 주식회사 드림
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
        date_col = f'구독개시일'
        date_col = f'교체신청일'
        if pd.notna(row[date_col]):
            formatted_date = format_date(row[date_col])
            if formatted_date:
                changes.append(f"{formatted_date}")

    # Join changes into a string
    교체정보 = ', '.join(changes)

    # Fill the template with the adjusted row data
    case_text = template.format(
        고객명=row['고객명'],
        가입회선=row['가입회선'],
        구독개시일=format_date(row['구독개시일']),
        교체신청일=format_date(row['교체신청일']),
    )
    
    # Append the case text to the all cases text
    all_cases_text += case_text + "\n\n"

# Define the output file path
output_file_path = r"C:\Users\DeokHwangbo\Downloads\py\Project_BT\Plastics\위드에스엠_해지통보.txt"

# Write the combined text to the file
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(all_cases_text)

print(f"텍스트 파일 작성완료!: {output_file_path}")