from datetime import datetime
from workalendar.asia import SouthKorea

def check_date_type(date=None):
    """날짜 타입을 확인하고 반환하는 함수"""
    # 현재 날짜 정보 가져오기
    current_date = None
    today_date = None

    if date is None:
        current_date = datetime.now()
        today_date = current_date.strftime('%Y-%m-%d 오전 12:00:00')
    else:
        current_date = datetime.strptime(date, '%Y-%m-%d 오전 12:00:00')
        today_date = date

    # 공휴일 체크
    kr_calendar = SouthKorea()
    is_holiday = kr_calendar.is_holiday(current_date.date())
    is_weekend = current_date.weekday() >= 5  # 5: 토요일, 6: 일요일

    print(f"Processing date: {today_date}")

    return today_date, is_holiday, is_weekend