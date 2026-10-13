"""조선시대 판별고사 — 요즘 말과 유행을 얼마나 아는지 판별하는 퀴즈 (Streamlit)."""
import html
import json
import random
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="조선시대 판별고사", page_icon="📜", layout="centered")

DATA = json.loads((Path(__file__).parent / "questions.json").read_text(encoding="utf-8"))
QUESTIONS = DATA["questions"]
LEVELS = DATA["levels"]
PICK = DATA["pick"]          # 영역별 출제 수 {"유행 문화": 6, "유행어": 6, "요즘 말투": 3}
SET_SIZE = DATA["set"]       # 한 판 문항 수 (15)
LETTERS = "ABCD"

# ---------------------------------------------------------------- 디자인
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=IBM+Plex+Sans+KR:wght@400;500;700&family=DM+Mono:wght@500&display=swap');
:root{
  --bg:#F2F0FB; --paper:#FFFFFF; --ink:#1D1A35; --muted:#6B6788; --line:#DCD8EE;
  --accent:#3B4CE0; --sticker:#FFE14D; --sticker-ink:#2A2300;
  --good:#1E9E6A; --good-bg:#E3F6EC; --bad:#D9364F; --bad-bg:#FDE7EA;
  --display:"Black Han Sans","IBM Plex Sans KR",sans-serif;
  --body:"IBM Plex Sans KR","Apple SD Gothic Neo",system-ui,sans-serif;
  --mono:"DM Mono",ui-monospace,Menlo,monospace;
}
html, body, .stApp, [data-testid="stAppViewContainer"]{background:var(--bg)!important;color:var(--ink);font-family:var(--body)}
#MainMenu, header[data-testid="stHeader"], footer, [data-testid="stToolbar"], [data-testid="stDecoration"]{display:none!important}
.block-container, [data-testid="stMainBlockContainer"]{max-width:680px!important;padding-top:2.2rem!important;padding-bottom:3rem!important}
.stApp p, .stApp li, .stApp span, .stApp div{font-family:var(--body)}

/* 시험지 카드 */
.st-key-sheet{background:var(--paper);border:1.5px solid var(--line);border-radius:22px;padding:28px 26px!important;gap:16px}
@media (max-width:520px){.st-key-sheet{padding:22px 18px!important}}

.eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.08em;color:var(--muted);text-transform:uppercase;margin:0}
.title{font-family:var(--display);font-weight:400;font-size:clamp(40px,9.5vw,58px);line-height:1.08;margin:6px 0 0;color:var(--ink)}
.title mark{background:var(--sticker);color:var(--sticker-ink);padding:0 .12em;border-radius:6px;display:inline-block;transform:rotate(-2deg)}
.lede{color:var(--muted);font-size:16px;line-height:1.65;margin:0}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{font-size:13px;font-weight:500;border:1.5px solid var(--line);border-radius:999px;padding:4px 12px;color:var(--muted)}
.areas{border-top:1.5px dashed var(--line);padding-top:16px;display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
@media (max-width:520px){.areas{grid-template-columns:1fr}}
.areas div{font-size:14px;color:var(--muted);line-height:1.5}
.areas b{display:block;font-family:var(--display);font-weight:400;font-size:19px;color:var(--ink)}

/* 문항 */
.qtop{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;font-family:var(--mono);font-size:13px;color:var(--muted)}
.cat{font-family:var(--body);font-weight:700;font-size:12px;color:var(--accent);border:1.5px solid var(--accent);border-radius:999px;padding:2px 10px}
.bar{height:8px;background:var(--line);border-radius:999px;overflow:hidden;margin-top:10px}
.bar i{display:block;height:100%;background:var(--accent);border-radius:999px}
.qtext{font-family:var(--display);font-weight:400;font-size:clamp(22px,5.4vw,29px);line-height:1.32;margin:4px 0 0;color:var(--ink)}
.word{display:inline-block;font-family:var(--display);font-size:clamp(28px,7.5vw,40px);line-height:1.15;background:var(--sticker);color:var(--sticker-ink);padding:4px 14px;border-radius:10px;transform:rotate(-1.5deg);margin:6px 0 4px}

/* 보기 버튼 */
.st-key-opts .stButton button{
  width:100%;min-height:58px;justify-content:flex-start;text-align:left;
  background:var(--paper)!important;color:var(--ink)!important;
  border:1.5px solid var(--line)!important;border-radius:14px!important;
  padding:12px 16px!important;font-size:15.5px;font-weight:500;
  transition:transform .12s, border-color .12s;box-shadow:none!important}
.st-key-opts .stButton button:hover{border-color:var(--accent)!important;transform:translateY(-1px)}
.st-key-opts .stButton button p{text-align:left;font-size:15.5px}

/* 채점된 보기 */
.opt{display:flex;gap:10px;align-items:flex-start;border:1.5px solid var(--line);border-radius:14px;padding:13px 16px;margin-bottom:10px;font-size:15.5px;color:var(--ink);background:var(--paper)}
.opt .n{font-family:var(--mono);color:var(--muted)}
.opt.right{border-color:var(--good);background:var(--good-bg)}
.opt.wrong{border-color:var(--bad);background:var(--bad-bg)}
.opt.dim{opacity:.55}
.fb{border-radius:14px;padding:14px 16px;font-size:15px;line-height:1.6}
.fb.ok{background:var(--good-bg)} .fb.no{background:var(--bad-bg)}
.fb strong{display:block;color:var(--good);margin-bottom:2px} .fb.no strong{color:var(--bad)}

/* 기본 버튼 */
.stButton button[kind="primary"], [data-testid="stBaseButton-primary"]{
  background:var(--accent)!important;color:#fff!important;border:0!important;
  border-radius:14px!important;min-height:56px;font-weight:700!important;font-size:17px!important;
  transition:transform .12s;box-shadow:none!important}
.stButton button[kind="primary"]:hover, [data-testid="stBaseButton-primary"]:hover{transform:translateY(-2px)}
.stButton button[kind="primary"] p{font-size:17px;font-weight:700}
.st-key-again .stButton button{min-height:56px;border-radius:14px!important;border:1.5px solid var(--line)!important;background:transparent!important;color:var(--ink)!important;font-weight:700}

/* 결과 */
.verdict{font-family:var(--mono);font-size:13px;color:var(--muted);margin:0}
.level{display:inline-block;font-family:var(--display);font-size:clamp(34px,9vw,48px);line-height:1.15;background:var(--sticker);color:var(--sticker-ink);padding:4px 16px;border-radius:12px;transform:rotate(-1.5deg);margin:8px 0 6px}
.score{font-family:var(--display);font-size:22px;color:var(--muted)}
.score b{font-weight:400;font-size:46px;color:var(--accent)}
.ladder{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
@media (max-width:520px){.ladder{grid-template-columns:repeat(2,1fr)}}
.ladder div{border:1.5px solid var(--line);border-radius:12px;padding:9px 11px;font-size:13px;color:var(--muted);line-height:1.45}
.ladder div b{display:block;color:var(--ink);font-size:14px}
.ladder div.on{border-color:var(--accent);background:var(--bg)}
.ladder div.on b{color:var(--accent)}
.rvhead{font-weight:700;font-size:16px;margin:4px 0 0}
.rv{border-left:4px solid var(--bad);padding:4px 0 4px 12px;margin-bottom:12px}
.rv b{display:block;font-family:var(--display);font-weight:400;font-size:20px}
.rv span{display:block;color:var(--muted);font-size:14px;line-height:1.55}
.foot{text-align:center;font-size:13px;color:var(--muted);margin-top:18px}
[data-testid="stCode"] pre, .stCode pre{border-radius:12px!important}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

esc = html.escape


# ---------------------------------------------------------------- 상태
def init_state():
    defaults = {"stage": "intro", "order": [], "i": 0, "score": 0, "wrong": [],
                "picked": None, "options": [], "seen": []}
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)


def draw_set():
    """영역별로 정해진 수만큼 뽑되, 이번 세션에서 안 나온 문제를 먼저 뽑는다."""
    seen = set(st.session_state.seen)
    picked = []
    for cat, n in PICK.items():
        pool = [i for i, q in enumerate(QUESTIONS) if q["c"] == cat]
        fresh = [i for i in pool if i not in seen]
        old = [i for i in pool if i in seen]
        random.shuffle(fresh)
        random.shuffle(old)
        picked += (fresh + old)[:n]
    if len(picked) < SET_SIZE:
        rest = [i for i in range(len(QUESTIONS)) if i not in picked]
        random.shuffle(rest)
        picked += rest[: SET_SIZE - len(picked)]
    if len(seen | set(picked)) >= len(QUESTIONS):
        seen = set()
    st.session_state.seen = list(seen | set(picked))
    random.shuffle(picked)
    return picked


def shuffled_options(qi):
    q = QUESTIONS[qi]
    opts = [q["a"], *q["d"]]
    random.shuffle(opts)
    return opts


def start():
    st.session_state.order = draw_set()
    st.session_state.i = 0
    st.session_state.score = 0
    st.session_state.wrong = []
    st.session_state.picked = None
    st.session_state.options = shuffled_options(st.session_state.order[0])
    st.session_state.stage = "quiz"


def choose(text):
    q = QUESTIONS[st.session_state.order[st.session_state.i]]
    st.session_state.picked = text
    if text == q["a"]:
        st.session_state.score += 1
    else:
        st.session_state.wrong.append(st.session_state.order[st.session_state.i])


def go_next():
    st.session_state.i += 1
    st.session_state.picked = None
    if st.session_state.i >= len(st.session_state.order):
        st.session_state.stage = "result"
    else:
        st.session_state.options = shuffled_options(st.session_state.order[st.session_state.i])


def level_for(score):
    lv = LEVELS[0]
    for l in LEVELS:
        if score >= l["min"]:
            lv = l
    return lv


# ---------------------------------------------------------------- 화면
def intro():
    with st.container(key="sheet"):
        st.markdown(
            """
<p class="eyebrow">2026학년도 시대 감별 영역</p>
<h1 class="title">혹시 조선시대에서<br><mark>오셨어요?</mark></h1>
""",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
<p class="lede">요즘 말과 유행을 얼마나 아는지 {SET_SIZE}문제로 판별해요. {len(QUESTIONS)}문제 문제은행에서 매번 다른 문제가 랜덤으로 나와요.
점수가 낮을수록 조선시대 사람, 높을수록 2026년 사람! 친구랑 같이 풀고 누가 진짜 조선시대 사람인지 가려 보세요.</p>
<div class="chips"><span class="chip">{len(QUESTIONS)}문제 중 {SET_SIZE}문제 랜덤</span><span class="chip">보기도 전부 진짜</span><span class="chip">2026년 10월 기준</span></div>
""",
            unsafe_allow_html=True,
        )
        st.button("판별 시작하기", type="primary", use_container_width=True, on_click=start)
        st.markdown(
            """
<div class="areas">
  <div><b>유행어</b>뜻 말고 쓰임새를 물어봐요</div>
  <div><b>요즘 말투</b>지금 쓰면 촌스러운 말은?</div>
  <div><b>유행 문화</b>앱, 디저트, 밈의 정체</div>
</div>
""",
            unsafe_allow_html=True,
        )


def quiz():
    s = st.session_state
    qi = s.order[s.i]
    q = QUESTIONS[qi]
    total = len(s.order)
    done = s.i + (1 if s.picked is not None else 0)

    with st.container(key="sheet"):
        st.markdown(
            f"""
<div class="qtop"><span>문항 {s.i + 1} / {total}</span><span class="cat">{esc(q['c'])}</span><span>맞힌 문제 {s.score}</span></div>
<div class="bar"><i style="width:{done / total * 100:.1f}%"></i></div>
<p class="qtext">{esc(q['q'])}</p>
<span class="word">{esc(q['w'])}</span>
""",
            unsafe_allow_html=True,
        )

        opts = s.options
        long_layout = q.get("long") or any(len(t) > 16 for t in opts)

        if s.picked is None:
            with st.container(key="opts"):
                if long_layout:
                    for k, t in enumerate(opts):
                        st.button(f"{LETTERS[k]}   {t}", key=f"o{s.i}_{k}", use_container_width=True,
                                  on_click=choose, args=(t,))
                else:
                    for row in range(0, len(opts), 2):
                        cols = st.columns(2, gap="small")
                        for c, k in zip(cols, range(row, row + 2)):
                            with c:
                                st.button(f"{LETTERS[k]}   {opts[k]}", key=f"o{s.i}_{k}",
                                          use_container_width=True, on_click=choose, args=(opts[k],))
        else:
            ok = s.picked == q["a"]
            rows = []
            for k, t in enumerate(opts):
                cls = "right" if t == q["a"] else ("wrong" if t == s.picked else "dim")
                rows.append(f'<div class="opt {cls}"><span class="n">{LETTERS[k]}</span><span>{esc(t)}</span></div>')
            st.markdown("".join(rows), unsafe_allow_html=True)
            head = "정답! 2026년 사람 인정" if ok else "땡! 조선시대 의심 +1"
            st.markdown(
                f'<div class="fb {"ok" if ok else "no"}"><strong>{head}</strong>{esc(q["x"])}</div>',
                unsafe_allow_html=True,
            )
            last = s.i == total - 1
            st.button("판별 결과 보기" if last else "다음 문제", type="primary",
                      use_container_width=True, on_click=go_next)


def result():
    s = st.session_state
    lv = level_for(s.score)
    with st.container(key="sheet"):
        ladder = []
        for k, l in enumerate(LEVELS):
            hi = LEVELS[k + 1]["min"] - 1 if k < len(LEVELS) - 1 else SET_SIZE
            on = " on" if l is lv else ""
            ladder.append(f'<div class="{on.strip()}"><b>{esc(l["name"])}</b>{l["min"]}~{hi}점</div>')
        st.markdown(
            f"""
<p class="verdict">판별 결과, 당신은</p>
<span class="level">{esc(lv['name'])}</span>
<div class="score"><b>{s.score}</b> / {len(s.order)}</div>
<p class="lede">{esc(lv['desc'])}</p>
<div class="ladder">{''.join(ladder)}</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown('<p class="rvhead">친구 도발용 문구 (오른쪽 위 버튼으로 복사)</p>', unsafe_allow_html=True)
        st.code(
            f"[조선시대 판별고사] 나는 {len(s.order)}문제 중 {s.score}개 맞혀서 '{lv['name']}' 판정! "
            f"너는 진짜 조선시대 사람 아니야?",
            language=None,
            wrap_lines=True,
        )

        with st.container(key="again"):
            st.button("다시 풀기 (새 문제로)", use_container_width=True, on_click=start)

        if s.wrong:
            parts = ['<p class="rvhead">틀린 문제로 현대 적응하기</p>']
            for qi in s.wrong:
                q = QUESTIONS[qi]
                parts.append(
                    f'<div class="rv"><b>{esc(q["w"])}</b><span>정답: {esc(q["a"])}</span>'
                    f'<span>{esc(q["x"])}</span></div>'
                )
            st.markdown("".join(parts), unsafe_allow_html=True)
        else:
            st.markdown('<p class="rvhead">만점! 틀린 문제가 하나도 없어요.</p>', unsafe_allow_html=True)


init_state()
{"intro": intro, "quiz": quiz, "result": result}[st.session_state.stage]()
st.markdown(
    '<p class="foot">2026년 기사와 트렌드 뉴스레터에 소개된 말과 유행을 바탕으로 만들었어요. 유행은 금방 바뀌니 재미로 봐 주세요.</p>',
    unsafe_allow_html=True,
)
