# 조선시대 판별고사

요즘 말과 유행을 얼마나 아는지 15문제로 판별하는 Streamlit 퀴즈 앱이에요.
50문제 문제은행에서 매번 유행 문화 6 · 유행어 6 · 요즘 말투 3문제를 랜덤으로 뽑아요.

## 파일 구성
- `app.py` — 화면과 퀴즈 진행 로직
- `questions.json` — 문제 50개와 판정 등급 (문제 추가·수정은 여기서)
- `requirements.txt` — 필요한 패키지
- `.streamlit/config.toml` — 기본 색상 테마

## 판정 기준 (15문제 기준)
| 점수 | 판정 |
|---|---|
| 0~4 | 조선시대 사람 |
| 5~8 | 2010년대 사람 |
| 9~12 | 2025년 사람 |
| 13~15 | 2026년 현역 |

## 인터넷에 올리기 (Streamlit Community Cloud)
1. GitHub에 새 저장소를 만들고 이 폴더의 파일을 모두 올려요 (`.streamlit` 폴더 포함).
2. share.streamlit.io 에 GitHub 계정으로 로그인해요.
3. Create app → 방금 만든 저장소 선택 → Main file path에 `app.py` → Deploy.
