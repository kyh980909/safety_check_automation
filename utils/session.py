import requests
import re
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 민감한 정보 가져오기
lab_no = os.getenv('LAB_NO')
login_id = os.getenv('LOGIN_ID')
login_pw = os.getenv('LOGIN_PW')

def get_session():
    """로그인 세션을 생성하고 반환하는 함수"""
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
        # print('처음 받은 쿠키 : ',cookies)

        # print('userCheck.do\n')
        user_check = s.post(user_check_url, data=login_info, headers=headers, cookies=cookies)
        
        # print('ajaxActionLogin2.do\n')
        ajax_login = s.post(ajax_login_url, data=login_info, headers=headers, cookies=cookies,
        allow_redirects=False)

        # print('token2.do\n')
        sso_login = s.post(sso_login_url, data=sso_login_info, headers=headers, cookies=cookies,
        allow_redirects=False)

        pattern = r'access_token=([^;]+)|refresh_token=([^;]+)'
        tokens = re.findall(pattern, sso_login.headers['Set-Cookie'])
        access_token, refresh_token = tokens[0][0], tokens[1][1]
        token = {"Cookie":f"access_token={access_token};refresh_token={refresh_token}"}

        # print('Get Session\n')
        final_login = s.post(session_url, data={"empid":"6aiFuENts/V0eaHMLdAyKw=="}, cookies=token, allow_redirects=False)
        session = {'Cookie': sso_login.headers['Set-Cookie'].split(';')[0] + 
                    final_login.headers['Set-Cookie'].split(';')[0]}

        s.get("https://safety.mju.ac.kr/Safety/LabCheckDayly/IsLabCheckGroup", cookies=token)

        check_cookies = {'Cookie':final_login.headers['Set-Cookie'].split(';')[0]+f';headerLastSelectLabNo={lab_no}'+';'+refresh_token}
        
        return s, check_cookies, headers 