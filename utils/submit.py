import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 민감한 정보 가져오기
lab_no = os.getenv('LAB_NO')

def submit_weekday(session, cookies, headers, today_date):
    """평일 안전점검 제출 함수"""
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

    response = session.post('https://safety.mju.ac.kr/Safety/LabCheckDayly/CreateOnLineAjx',
                  data=check_data,
                  cookies=cookies,
                  headers=headers)
    return response

def submit_weekend_holiday(session, cookies, headers, today_date):
    """주말/공휴일 안전점검 제출 함수"""
    check_data = {
        'LabNo': lab_no,
        'AskDay': today_date
    }

    response = session.post('https://safety.mju.ac.kr/Safety/LabCheckDayly/CreateOnLine_NA',
                  data=check_data,
                  cookies=cookies,
                  headers=headers)
    return response 