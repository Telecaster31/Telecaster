import pandas as pd

# Load the Excel file
file_path = r"C:\Users\DeokHwangbo\Downloads\강제해지SMS\(USM&보험재가입)강제해지LIST.xlsx"
df = pd.read_excel(file_path, dtype={'cancel_subscription_date': str, 'swap_date': str, 'exp_date': str})

# Fill NaN values with empty strings
df = df.fillna('')

# Define the template texts
template_normal = """[LG U+ 맘대로 폰교체]

{고객명} 고객님 안녕하세요, 맘대로 폰교체 고객센터입니다.

당사는 맘대로폰교체 서비스 이용약관 제4조 2항 14호에 “가입 신청한 휴대폰과 사용중인 휴대폰이 다른 경우” 서비스 가입을 제한할 수 있음을 밝히고 있습니다.

귀하께서 맘대로폰교체 서비스에 가입한 이후 귀하의 가입 단말기 ({단말기명}, 일련번호 {일련번호})에
본인 명의의 회선({해지구독회선})의 USIM을 장착한 이력이 전혀 없는 것을 확인하였습니다.

귀하께서 맘대로폰교체 서비스에 가입하신 {해지구독일자} 이후 귀하께서 맘대로폰교체 서비스에 등록한 단말기(일련번호 {일련번호})에
등록휴대번호({해지구독회선})의 USIM을 장착한 이력이 없다는 사실은
귀하께서 본 서비스에 가입 신청하신 휴대폰과 사용중인 휴대폰이 다른 경우에 해당함을 뜻합니다.

당사는 귀하께 이에 대해 소명하고 귀하의 등록휴대폰이 귀하께서 사용하고 계신 휴대폰이라는 증빙자료를 제출하실 기회를 드렸으나,
귀하께서는 등록휴대폰을 분실하였음을 주장하시는 것 외에 맘대로폰교체 가입 당시에 본인이 등록휴대폰을 실제로 사용하고 있었음을 뒷받침해 줄 수 있는 자료를 제출하지 않으셨습니다.

따라서 당사는 귀하께서 맘대로폰교체 서비스에 등록하신 단말기는 가입이 불가능한 단말기인 것으로 판단하였습니다.
이런 사유로 당사는 귀하께서 유지 중인 맘대로폰교체 구독을 해지하기로 하였으며 구독이 해지됨에 따라 신청하신 교체 휴대폰은 제공 드릴 수 없습니다.
{해지구독회선} 회선에 대한 본 서비스 구독을 해지하고 기납부하신 교체수수료와 월이용료를 환불해 드리겠습니다.

감사합니다.
볼트테크코리아 주식회사 드림.
"""

template_exp = """[LG U+ 맘대로 폰교체]

{고객명} 고객님 안녕하세요, 맘대로 폰교체 고객센터입니다.

당사는 맘대로폰교체 서비스 이용약관 제4조 2항 14호에 “가입 신청한 휴대폰과 사용중인 휴대폰이 다른 경우” 서비스 가입을 제한할 수 있음을 밝히고 있습니다.

귀하께서 맘대로폰교체 서비스에 가입한 이후 귀하의 가입 단말기 ({단말기명}, 일련번호 {일련번호})에
본인 명의의 회선({해지구독회선})의 USIM을 장착한 이력이 전혀 없는 것을 확인하였습니다.

귀하께서 맘대로폰교체 서비스에 가입하신 {해지구독일자} 이후 귀하께서 맘대로폰교체 서비스에 등록한 단말기(일련번호 {일련번호})에
등록휴대번호({해지구독회선})의 USIM을 장착한 이력이 없다는 사실은
귀하께서 본 서비스에 가입 신청하신 휴대폰과 사용중인 휴대폰이 다른 경우에 해당함을 뜻합니다.

당사는 귀하께 이에 대해 소명하고 귀하의 등록휴대폰이 귀하께서 사용하고 계신 휴대폰이라는 증빙자료를 제출하실 기회를 드렸으나,
귀하를 대신하여 '{대리소명인}'님께서 {소명일자}에 이메일로 답변을 보내셨습니다.
'{대리소명인}'님은 단말기 분실을 주장하셨으나, 귀하께서 본인에게 귀하를 대신하여 당사와의 연락을 취하는 것에 대해 동의하셨다는 어떤 설명이나 증빙자료도 제시하지 않았고,
귀하께서 맘대로폰교체 서비스에 가입하신 {해지구독일자} 및 그 후에 이 휴대폰을 사용하셨다는 증빙이 될 수 있는 자료를 제출하지 않으셨습니다.

따라서 당사는 귀하께서 맘대로폰교체 서비스에 등록하신 단말기는 가입이 불가능한 단말기인 것으로 판단하였습니다.
이런 사유로 당사는 귀하께서 유지 중인 맘대로폰교체 구독을 해지하기로 하였으며 구독이 해지됨에 따라 신청하신 교체 휴대폰은 제공 드릴 수 없습니다.
{해지구독회선} 회선에 대한 본 서비스 구독을 해지하고 기납부하신 교체수수료와 월이용료를 환불해 드리겠습니다.

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

# Loop through each row in the dataframe
for index, row in df.iterrows():
    # Choose the appropriate template based on the 'exp' column
    if row['exp'] == 'Y':
        template = template_exp
    else:
        template = template_normal
    
    # Fill the template with the adjusted row data
    case_text = template.format(
        고객명=row['customer_name'],
        해지구독회선=row['cancel_subscription_line'],
        해지구독일자=format_date(row['cancel_subscription_date']),
        단말기명=row['device_name'],
        일련번호=row['device_num'],
        대리소명인=row['explainer'],
        소명일자=format_date(row['exp_date'])  # Apply formatting to swap_date
    )
    
    # Append the case text to the all cases text
    all_cases_text += case_text + "\n\n"

# Define the output file path
output_file_path = r"C:\Users\DeokHwangbo\Downloads\강제해지SMS\20250415_서동헌_강제해지SMS.txt"

# Write the combined text to the file
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(all_cases_text)

print(f"텍스트 파일 작성완료!: {output_file_path}")