# Auto Safety Check

명지대학교 실험실 안전점검 자동화 스크립트

## 설치 방법

1. 필요한 패키지 설치:

```bash
pip install -r requirements.txt
```

2. 환경 변수 설정:

- `.env.example` 파일을 `.env`로 복사
- `.env` 파일에 다음 정보 입력:
  ```
  LAB_NO=your_lab_number
  LOGIN_ID=your_login_id
  LOGIN_PW=your_password
  ```

## 사용 방법

```bash
python auto_safety_check.py
```

## 주의사항

- `.env` 파일은 절대로 Git에 커밋하지 마세요!
- 비밀번호는 안전하게 관리하세요.
- 이 스크립트는 개인적인 용도로만 사용하세요.
