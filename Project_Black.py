import pandas as pd
import pyzipper
import os
from datetime import datetime, timedelta

# 어제 날짜 계산 & 'YYYYMMDD' 형식으로 날짜 변환
yesterday = datetime.now() - timedelta(1)
yesterday_str = yesterday.strftime('%Y%m%d')

# 디렉토리 경로 설정
directory_path = r"C:\Users\DeokHwangbo\Downloads"

# 디렉토리 내에서 'csv.zip' 파일을 필터링하고, 키워드에 따라 경로를 설정
customer_zip_file_path = None
subscription_zip_file_path = None
swap_zip_file_path = None

for file_name in os.listdir(directory_path):
    if 'csv.zip' in file_name:
        if 'customer' in file_name:
            customer_zip_file_path = os.path.join(directory_path, file_name)
        elif 'subscription' in file_name:
            subscription_zip_file_path = os.path.join(directory_path, file_name)
        elif 'swap' in file_name:
            swap_zip_file_path = os.path.join(directory_path, file_name)

# 압축 파일 내의 파일 경로 설정
customer_file_in_zip = f'data-export-{customer_zip_file_path.split("data-export-")[1]}'.replace('.zip', '')
subscription_file_in_zip = f'data-export-{subscription_zip_file_path.split("data-export-")[1]}'.replace('.zip', '')
swap_file_in_zip = f'data-export-{swap_zip_file_path.split("data-export-")[1]}'.replace('.zip', '')

# 압축 파일 비밀번호 설정
password = b"fknr46fd2EQH"

# 압축 파일 내의 CSV 파일을 읽어오기
with pyzipper.AESZipFile(customer_zip_file_path, 'r') as z:
    z.setpassword(password)
    with z.open(customer_file_in_zip) as f:
        df_customers = pd.read_csv(f, on_bad_lines='skip', low_memory=False)
        
with pyzipper.AESZipFile(subscription_zip_file_path, 'r') as z:
    z.setpassword(password)
    with z.open(subscription_file_in_zip) as f:
        df_subscriptions = pd.read_csv(f, on_bad_lines='skip', low_memory=False)
        
with pyzipper.AESZipFile(swap_zip_file_path, 'r') as z:
    z.setpassword(password)
    with z.open(swap_file_in_zip) as f:
        df_swaps = pd.read_csv(f, on_bad_lines='skip', low_memory=False)

# 블랙리스트가 True인 행 조회
blacklist_df = df_customers[df_customers['blacklisted'] == True]

# 블랙리스트된 고객 ID 추출
blacklisted_ids = blacklist_df['_id']

# 공통 조건에 맞는 데이터 필터링 (subscriptions의 status가 active인 경우만 포함)
filtered_subscriptions_df = df_subscriptions[(df_subscriptions['customerId'].isin(blacklisted_ids)) & (df_subscriptions['status'] == 'active')]

# 컴플리트된 swap만 추출
filtered_swaps_df = df_swaps[(df_swaps['customerId'].isin(blacklisted_ids)) & (df_swaps['status'] == 'completed')]

# Blacklist 데이터프레임에서 필요한 열만 추출 (예: _id, contact.lastName, contact.dateOfBirth)
blacklist_filtered_df = blacklist_df[['_id', 'contact.lastName', 'contact.dateOfBirth']]

# filtered_subscriptions_df와 blacklist_filtered_df를 customerId를 기준으로 병합
merged_subscriptions_df = pd.merge(filtered_subscriptions_df, blacklist_filtered_df, left_on='customerId', right_on='_id', how='left')

# filtered_swaps_df와 blacklist_filtered_df를 customerId를 기준으로 병합
merged_swaps_df = pd.merge(filtered_swaps_df, blacklist_filtered_df, left_on='customerId', right_on='_id', how='left')

# NAME과 DOB 열을 조건에 맞게 병합하여 새로운 열 생성
merged_subscriptions_df['NAME_DOB'] = merged_subscriptions_df['contact.lastName'] + '/' + merged_subscriptions_df['contact.dateOfBirth']
merged_swaps_df['NAME_DOB'] = merged_swaps_df['contact.lastName'] + '/' + merged_swaps_df['contact.dateOfBirth']

# NAME_DOB 열에서 오른쪽 14글자 제외
merged_subscriptions_df['NAME_DOB'] = merged_subscriptions_df['NAME_DOB'].str[:-14]
merged_swaps_df['NAME_DOB'] = merged_swaps_df['NAME_DOB'].str[:-14]
df_customers['NAME_DOB'] = df_customers['contact.lastName'] + '/' + df_customers['contact.dateOfBirth']
df_customers['NAME_DOB'] = df_customers['NAME_DOB'].str[:-14]

# 병합된 데이터프레임과 CUSTOMER 파일을 NAME_DOB를 기준으로 병합하여 일치하는 데이터만 선택
final_merged_subscriptions_df = pd.merge(df_customers, merged_subscriptions_df[['NAME_DOB']], on='NAME_DOB', how='inner')
final_merged_swaps_df = pd.merge(df_customers, merged_swaps_df[['NAME_DOB']], on='NAME_DOB', how='inner')

# Subscriptions 파일에서 final_merged_df와 동일한 customer ID를 가진 데이터 중에서 status가 active인 데이터 추출
final_filtered_subscriptions_df = df_subscriptions[(df_subscriptions['customerId'].isin(final_merged_subscriptions_df['_id'])) & (df_subscriptions['status'] == 'active')]

# Swaps 파일에서 final_merged_df와 동일한 customer ID를 가진 데이터 중에서 status가 completed인 데이터 추출
final_filtered_swaps_df = df_swaps[(df_swaps['customerId'].isin(final_merged_swaps_df['_id'])) & (df_swaps['status'] == 'completed')]

# final_merged_df에서 customerId와 NAME_DOB를 추출하여 df_subscriptions에 추가
final_filtered_subscriptions_df = pd.merge(final_filtered_subscriptions_df, final_merged_subscriptions_df[['_id', 'NAME_DOB']], left_on='customerId', right_on='_id', how='left')
final_filtered_swaps_df = pd.merge(final_filtered_swaps_df, final_merged_swaps_df[['_id', 'NAME_DOB']], left_on='customerId', right_on='_id', how='left')

# 필요한 열만 선택하고 열 이름 변경
final_filtered_subscriptions_df = final_filtered_subscriptions_df[['NAME_DOB', 'customerId', '_id_x', 'phoneNumber', 'activationDate', 'status', 'device.sku', 'shopCode']]
final_filtered_subscriptions_df = final_filtered_subscriptions_df.rename(columns={'_id_x': 'subscriptionId'})
final_filtered_subscriptions_df = final_filtered_subscriptions_df.rename(columns={'device.sku': 'SKU'})
final_filtered_subscriptions_df['activationDate'] = final_filtered_subscriptions_df['activationDate'].str[:-14]

# 'SubscriptionID' 기준으로 중복된 값 제거
final_filtered_subscriptions_df = final_filtered_subscriptions_df.drop_duplicates(subset=['subscriptionId'])

# swapId 열을 추가하여 final_filtered_swaps_df 생성
final_filtered_swaps_df = final_filtered_swaps_df[['NAME_DOB', 'customerId', 'subscriptionId', 'number', 'status', 'approvedAt', 'completedAt', 'usageType']]
final_filtered_swaps_df = final_filtered_swaps_df.rename(columns={'number': 'SPO number'})
final_filtered_swaps_df['approvedAt'] = final_filtered_swaps_df['approvedAt'].str[:-14]
final_filtered_swaps_df['completedAt'] = final_filtered_swaps_df['completedAt'].str[:-14]

# 'SPO number' 기준으로 중복된 값 제거
final_filtered_swaps_df = final_filtered_swaps_df.drop_duplicates(subset=['SPO number'])

# NAME_DOB를 기준으로 replace 횟수, switch 횟수, replace와 switch 합산 횟수 추가
replace_count = final_filtered_swaps_df[final_filtered_swaps_df['usageType'] == 'replace'].groupby('NAME_DOB').size().reset_index(name='replace_count')
switch_count = final_filtered_swaps_df[final_filtered_swaps_df['usageType'] == 'switch'].groupby('NAME_DOB').size().reset_index(name='switch_count')

# 두 데이터프레임을 병합하여 total_count를 계산
swap_counts = pd.merge(replace_count, switch_count, on='NAME_DOB', how='outer').fillna(0)
swap_counts['total_count'] = swap_counts['replace_count'] + swap_counts['switch_count']

# swap_counts를 final_filtered_swaps_df에 병합
final_filtered_swaps_df = pd.merge(final_filtered_swaps_df, swap_counts, on='NAME_DOB', how='left')

# 각 NAME_DOB에 대해 가장 큰 approvedAt와 두 번째로 큰 approvedAt 찾기
sorted_swaps_df = final_filtered_swaps_df.sort_values(by=['NAME_DOB', 'approvedAt'], ascending=[True, False])
top_2_approved_dates = sorted_swaps_df.groupby('NAME_DOB')['approvedAt'].apply(lambda x: x.iloc[:2].tolist()).reset_index()
top_2_approved_dates[['approvedAt_1st', 'approvedAt_2nd']] = pd.DataFrame(top_2_approved_dates['approvedAt'].tolist(), index=top_2_approved_dates.index)
top_2_approved_dates = top_2_approved_dates.drop(columns=['approvedAt'])

# 최종 데이터프레임에 병합
final_filtered_subscriptions_df = pd.merge(final_filtered_subscriptions_df, top_2_approved_dates, on='NAME_DOB', how='left')

# 날짜 형식 변환
final_filtered_subscriptions_df['activationDate'] = pd.to_datetime(final_filtered_subscriptions_df['activationDate'])
final_filtered_subscriptions_df['approvedAt_1st'] = pd.to_datetime(final_filtered_subscriptions_df['approvedAt_1st'])
final_filtered_subscriptions_df['approvedAt_2nd'] = pd.to_datetime(final_filtered_subscriptions_df['approvedAt_2nd'])

# 'CHECK' 열 추가
def check_condition(row):
    try:
        return (
            (row['activationDate'] - pd.DateOffset(days=365) < row['approvedAt_2nd'])
            and (row['activationDate'] > row['approvedAt_1st'])
            and (row['activationDate'] > row['approvedAt_2nd'])
        )
    except TypeError as e:
        print(f"TypeError: {e} in row: {row}")
        return False

final_filtered_subscriptions_df['CHECK'] = final_filtered_subscriptions_df.apply(check_condition, axis=1)

# 'swap' 열 추가 (Completed Swaps 시트에 없는 subscriptionId에 대해 'NO SWAP' 표시)
completed_swap_ids = final_filtered_swaps_df['subscriptionId'].unique()
final_filtered_subscriptions_df['swap'] = final_filtered_subscriptions_df.apply(
    lambda row: 'NO SWAP' if row['subscriptionId'] not in completed_swap_ids else '', axis=1
)

# 최종 데이터프레임을 엑셀 파일의 다른 시트로 저장 (파일명에 어제 날짜 포함)
output_file_path = fr"C:\Users\DeokHwangbo\Downloads\blacklist check\{yesterday_str}_blacklist.xlsx"
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

with pd.ExcelWriter(output_file_path) as writer:
    final_filtered_subscriptions_df.to_excel(writer, sheet_name='Active Subscriptions', index=False)
    final_filtered_swaps_df.to_excel(writer, sheet_name='Completed Swaps', index=False)

print(f"일치하는 데이터프레임이 {output_file_path} 파일로 저장되었습니다.")