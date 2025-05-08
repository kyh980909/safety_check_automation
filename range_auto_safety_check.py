from dotenv import load_dotenv
import os
from utils.session import get_session
from utils.submit import submit_weekday, submit_weekend_holiday
from utils.date_check import check_date_type
import logging
from datetime import datetime, timedelta

def run_safety_check(today_date):
    """안전점검 실행 함수"""
    try:
        # 날짜 타입 확인
        _, is_holiday, is_weekend = check_date_type(today_date)
        logger.info(f"날짜 확인 완료: {today_date}")

        # 세션 생성
        logger.info("로그인 세션 생성 중...")
        session, cookies, headers = get_session()
        logger.info("로그인 세션 생성 완료")

        # 날짜 타입에 따라 다른 API 호출
        if is_holiday or is_weekend:
            logger.info("주말/공휴일 안전점검 제출 중...")
            response = submit_weekend_holiday(session, cookies, headers, today_date)
        else:
            logger.info("평일 안전점검 제출 중...")
            response = submit_weekday(session, cookies, headers, today_date)

        # 응답 확인
        if response.status_code == 200:
            logger.info("안전점검 제출 성공")
            logger.debug(f"응답 내용: {response.text}")
        else:
            logger.error(f"안전점검 제출 실패 (상태 코드: {response.status_code})")
            logger.error(f"응답 내용: {response.text}")

    except Exception as e:
        logger.error(f"오류 발생: {str(e)}", exc_info=True)
        raise

def main(today_date):
    """메인 실행 함수"""
    try:
        logger.info("안전점검 자동화 스크립트 시작")
        run_safety_check(today_date)
        logger.info("안전점검 자동화 스크립트 종료")
    except Exception as e:
        logger.error("프로그램 실행 중 오류가 발생했습니다.", exc_info=True)
        raise

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 민감한 정보 가져오기
lab_no = os.getenv('LAB_NO')
login_id = os.getenv('LOGIN_ID')
login_pw = os.getenv('LOGIN_PW')

# 필수 환경 변수 체크
if not all([lab_no, login_id, login_pw]):
    raise ValueError("필수 환경 변수가 설정되지 않았습니다. .env 파일을 확인해주세요.")

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 시작 날짜와 끝 날짜 설정
start_date = datetime(2025, 5, 3)  # 시작 날짜 (YYYY, MM, DD)
end_date = datetime(2025, 5, 8)   # 끝 날짜 (YYYY, MM, DD)

# 날짜 범위 반복
current_date = start_date
while current_date <= end_date:
    today_date = current_date.strftime('%Y-%m-%d 오전 12:00:00')
    main(today_date)
    
    # 다음 날짜로 이동
    current_date += timedelta(days=1)
