# Problem of Week Web

## 실행 방법

1. `pipenv install`

2. `pipenv run dev`

## 개발

- 의존성 관리는 pipenv를 사용한다.
- VS Code가 pipenv 환경을 감지하지 못하는 경우, 커맨드 팔레트(Ctrl/Cmd + Shift + P)에서 "Python: Select Interpreter" 명령을 실행한다. problem-of-week-web 이름으로 된 pipenv 환경을 선택한다.
- 비밀 키, 개인정보 등 공개되면 안 되는 정보는 .env 파일에 저장하고 dotenv 라이브러리로 불러온다.

## 레퍼런스

- [Flask 홈페이지](https://flask.palletsprojects.com/en/2.0.x/)
