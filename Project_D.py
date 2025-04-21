from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument(r"--user-data-dir=C:\Users\DeokHwangbo\AppData\Local\Google\Chrome\User Data")
options.add_argument("--profile-directory=Default")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://admin.device.bolttech.kr")
input("로그인 확인 후 Enter 키를 누르세요...")

# 이제 자동화 코드 작성 가능
print("✅ 자동화 시작")
