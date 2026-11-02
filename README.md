# Study Deck

별명을 브라우저 `localStorage`에 저장해 사용하는 스터디 관리 앱입니다. 별명별로 할 일과 출석 기록이 분리됩니다. 로그인과 회원가입은 사용하지 않습니다.

이 프로젝트는 외부 AI 모델이나 대용량 모델 파일을 사용하지 않습니다. 별도로 준비할 모델은 없습니다.

## 실행

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

브라우저에서 http://127.0.0.1:8080 을 엽니다.

## 테스트

```powershell
pytest -q
```

Docker: `docker build -t studydeck .` 후 `docker run --rm -p 8080:8080 studydeck`.
