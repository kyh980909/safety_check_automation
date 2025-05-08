import requests
import re
from datetime import datetime
from workalendar.asia import SouthKorea
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 민감한 정보 가져오기
lab_no = os.getenv('LAB_NO')
login_id = os.getenv('LOGIN_ID')
login_pw = os.getenv('LOGIN_PW')

# 필수 환경 변수 체크
if not all([lab_no, login_id, login_pw]):
    raise ValueError("필수 환경 변수가 설정되지 않았습니다. .env 파일을 확인해주세요.")

# 현재 날짜 정보 가져오기
current_date = datetime.now()
today_date = current_date.strftime('%Y-%m-%d 오전 12:00:00')

# 공휴일 체크
kr_calendar = SouthKorea()
is_holiday = kr_calendar.is_holiday(current_date.date())
is_weekend = current_date.weekday() >= 5  # 5: 토요일, 6: 일요일

# 날짜 타입에 따른 메시지 출력
if is_holiday:
    holiday_name = kr_calendar.get_holiday_label(current_date.date())
    print(f"오늘은 공휴일입니다: {holiday_name}")
elif is_weekend:
    print("오늘은 주말입니다.")
else:
    print("오늘은 평일입니다.")

print(f"Processing date: {today_date}")

safety_check_url = f'https://safety.mju.ac.kr/Safety/LabCheckDayly/Index?LabNo={lab_no}'
login_page_url = 'https://sso1.mju.ac.kr/login.do?redirect_uri=http://safety.mju.ac.kr/sso/LoginCheck_SSO.aspx'
user_check_url = 'https://sso1.mju.ac.kr/mju/userCheck.do'
ajax_login_url = 'https://sso1.mju.ac.kr/login/ajaxActionLogin2.do'
sso_login_url = 'https://sso1.mju.ac.kr/oauth2/token2.do'
session_url = 'https://safety.mju.ac.kr/sso/SSO_OK.aspx'
        
login_info = {"id":login_id, "passwrd":login_pw}
sso_login_info = {"user_id":login_id, "user_pwd":login_pw, "client_id2":"", "redirect_uri": "http://safety.mju.ac.kr/sso/LoginCheck_SSO.aspx"}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://safety.mju.ac.kr',
    'Referer': f'https://safety.mju.ac.kr/Safety/LabCheckDayly/Index?LabNo={lab_no}',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"'
}
with requests.Session() as s:
    login_page = s.get(login_page_url, headers=headers)
    cookies = {"Cookie":login_page.headers['Set-Cookie'].split(';')[0]}
    print('처음 받은 쿠키 : ',cookies)

    print('userCheck.do\n')
    user_check = s.post(user_check_url, data=login_info, headers=headers, cookies=cookies)
    
    print('ajaxActionLogin2.do\n')
    ajax_login = s.post(ajax_login_url, data=login_info, headers=headers, cookies=cookies,
    allow_redirects=False)

    print('token2.do\n')
    sso_login = s.post(sso_login_url, data=sso_login_info, headers=headers, cookies=cookies,
    allow_redirects=False)

    pattern = r'access_token=([^;]+)|refresh_token=([^;]+)'
    tokens = re.findall(pattern, sso_login.headers['Set-Cookie'])
    access_token, refresh_token = tokens[0][0], tokens[1][1]
    token = {"Cookie":f"access_token={access_token};refresh_token={refresh_token}"}

    print('Get Session\n')
    final_login = s.post(session_url, data={"empid":"6aiFuENts/V0eaHMLdAyKw=="}, cookies=token, allow_redirects=False) # empid는 크롬 브라우저로 들어가서 개발자 툴에서 조회
    session = {'Cookie': sso_login.headers['Set-Cookie'].split(';')[0] + 
                final_login.headers['Set-Cookie'].split(';')[0]}

    s.get("https://safety.mju.ac.kr/Safety/LabCheckDayly/IsLabCheckGroup", cookies=token)

    check_cookies = {'Cookie':final_login.headers['Set-Cookie'].split(';')[0]+f';headerLastSelectLabNo={lab_no}'+';'+refresh_token}

    check_data = [
        ('LabNo', lab_no),
        ('LabCheckNo', '0'),
        ('AskDay', today_date),
        ('Proper_1', 'on'),
        ('ElementNo', '81'), ('Proper', '1'), ('Proper_1_81', '1'), ('Comment', ''),
        ('ElementNo', '82'), ('Proper', '1'), ('Proper_1_82', '1'), ('Comment', ''),
        ('ElementNo', '83'), ('Proper', '1'), ('Proper_1_83', '1'), ('Comment', ''),
        ('ElementNo', '84'), ('Proper', '1'), ('Proper_1_84', '1'), ('Comment', ''),
        ('ElementNo', '85'), ('Proper', '1'), ('Proper_1_85', '1'), ('Comment', ''),
        ('ElementNo', '86'), ('Proper', '1'), ('Proper_1_86', '1'), ('Comment', ''),
        ('Proper_2', 'on'),
        ('ElementNo', '87'), ('Proper', '1'), ('Proper_2_87', '1'), ('Comment', ''),
        ('ElementNo', '88'), ('Proper', '1'), ('Proper_2_88', '1'), ('Comment', ''),
        ('ElementNo', '89'), ('Proper', '1'), ('Proper_2_89', '1'), ('Comment', ''),
        ('ElementNo', '90'), ('Proper', '1'), ('Proper_2_90', '1'), ('Comment', ''),
        ('Proper_3', 'on'),
        ('ElementNo', '91'), ('Proper', '1'), ('Proper_3_91', '1'), ('Comment', ''),
        ('ElementNo', '92'), ('Proper', '1'), ('Proper_3_92', '1'), ('Comment', ''),
        ('ElementNo', '93'), ('Proper', '1'), ('Proper_3_93', '1'), ('Comment', ''),
    ]

    test = s.post('https://safety.mju.ac.kr/Safety/LabCheckDayly/CreateOnLineAjx',
                    data=check_data,
                    cookies=check_cookies,
                    headers=headers)

    print(test.headers)
    print(test.status_code)
    print(test.text)