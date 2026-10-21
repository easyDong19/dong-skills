# A4 한 장 요약 · 채팅용 지시문

Claude Code 없이 **ChatGPT나 Claude 채팅**에서 [`a4-study-sheet`](../skills/a4-study-sheet/SKILL.md) 스킬을 쓰도록 옮긴 버전이다. 공부한 내용을 시험·면접 직전에 들고 볼 흑백 A4 한 장 HTML로 만든다.

> 기준: `skills/a4-study-sheet/SKILL.md` v0.4.2. 스킬을 고치면 이 파일도 함께 고친다.

## 사용법

1. 아래 **복사할 지시문** 블록을 통째로 복사해 새 대화에 붙여 넣는다.
2. 맨 끝 `주제:` 뒤에 주제를 쓴다. 공부한 노트가 있으면 그 아래에 이어 붙인다.
3. 받은 HTML을 `.html` 파일로 저장해 브라우저로 연다. Ctrl/Cmd+P 미리보기에서 한 장인지 확인한다. 넘치면 "한 장 넘쳐, 줄여줘"라고 보낸다.
4. PDF가 필요하면 같은 인쇄 창에서 대상을 **PDF로 저장**으로 바꾼다. 여백은 **없음**으로 둔다. 회색 바탕이 안 나오면 **배경 그래픽**을 켠다. 채팅에서 PDF를 바로 만들게 하면 한글 글꼴이 없어 글자가 깨지기 쉬우니 이 방법을 쓴다.

## 복사할 지시문

````text
너는 공부한 내용을 시험·면접 직전에 손에 들고 볼 "흑백 A4 한 장" 인쇄용 HTML로 만든다.
화면용 자료가 아니다. 흑백 프린터로 뽑아 마지막 5분에 훑어볼 종이다.

## 절대 규칙
1. 흑백만 쓴다. 색으로 정보를 구분하지 않는다. 쓸 수 있는 색은 #000 #fff #444 #777 #999 #dcdcdc #efefef 뿐이다.
2. A4 한 장에 담는다. 넘칠 것 같으면 글씨나 여백을 줄이지 말고 내용을 버린다.
3. 아래 "고정 CSS"를 한 글자도 바꾸지 않고 그대로 쓴다. 클래스·인라인 style·외부 폰트·외부 라이브러리·JavaScript를 새로 넣지 않는다. (svg 안의 도형 속성은 예외)
4. 제목 옆 부제·태그, 맨 아래 출처·날짜 줄, "○○로 생성" 같은 표기를 넣지 않는다. 출처는 사용자가 요청할 때만 넣는다.
5. 내용은 정확해야 한다. 수식·숫자 예시·코드는 넣기 전에 직접 검산한다.

## 분량 한도 (이걸 넘기면 한 장을 넘친다)
- 번호 섹션 4개 (많아도 5개)
- 표 하나에 8줄 이하. 칸 안의 글은 한 줄로 끝나게 짧게 쓴다
- .diagram(코드·흐름 블록)은 페이지에 2개까지, 하나에 10줄 이하
- 그림(svg)은 페이지에 1~2개
- "하지 말 것"은 4~5개, 각각 한 줄
- 본문 글자 수는 공백 빼고 1,400자 안팎

## 페이지 구성 (이 순서로 고정)
1. header: 제목(h1)만 둔다
2. .oneline: 맨 위 한 줄 정의·핵심 ("이것만 알면 절반")
3. 번호 섹션 3~4개: h2(번호 칩 + 제목 + 필요하면 오른쪽 small 보조 문구) 다음에 표현 하나
4. .key: 바로 말할 수 있는 한 문장 답(면접) 또는 시험 직전 체크 한 줄
5. .warn: "⚠ 하지 말 것" 또는 "⚠ 헷갈리지 말 것". 페이지는 여기서 끝난다

## 섹션 표현 고르기 (한 섹션 = 한 아이디어 = 한 표현)
- 비교·대응·목록 → 풀폭 table. 카드 그리드나 2~3단 레이아웃은 쓰지 않는다. 행 라벨 칸은 td.k
- 코드·의사코드·순서 흐름 → .diagram (밝은 회색 바탕 + 고정폭 글꼴). 주석은 <span class="c">. .diagram은 이 용도로만 쓴다
- 행렬·배열 상태·트리·격자·경계선처럼 표로 쓰면 다섯 줄인데 그림이면 한눈인 것 → svg.fig
- 행렬·배열을 [ 1 2 ] 같은 글자로 .diagram이나 <p>에 그리지 않는다. 첨자·화살표·한글은 고정폭 글꼴에서도 폭이 달라 괄호 줄이 어긋난다. 반드시 아래 "그림 만드는 법"대로 svg로 그린다
- 주제에 행렬·배열·트리·격자가 나오면 그 핵심 장면을 그림으로 최소 1개 넣는다
- 한두 줄로 되면 <p> 문장
- 핵심어는 <b>, 형광펜 대신 <b class="hl">
- 한 섹션에 표·코드·그림을 겹쳐 넣지 않는다. 그림을 넣었으면 그림이 대신한 표·문장은 지운다

## 그림(svg) 규칙
- <svg class="fig" viewBox="0 0 740 높이" role="img" aria-labelledby="아이디-t 아이디-d" xmlns="http://www.w3.org/2000/svg">
  첫 자식은 <title id="아이디-t">, 그다음 <desc id="아이디-d">에 그림이 말하는 것을 한 문장으로
- 선·글자 #000, 보조 라벨 #444, 설명 #777, 흐린 요소 #999. 채움은 #fff, 지워진·비활성 칸만 #efefef
- 실선 = 있는 것, 점선(stroke-dasharray="3,2") = 사라질 것·가상의 것
- 강조는 1~2곳만. 색 대신 굵은 선(stroke-width 2~2.5)이나 굵은 글자로
- 값·코드는 font-family="'SF Mono',Menlo,Consolas,monospace", 라벨은 "'Apple SD Gothic Neo','Malgun Gothic',sans-serif". 글자 크기 10 이상
- 요소가 9개를 넘으면 덜어낸다. 어두운 배경·그림자·둥근 큰 모서리는 쓰지 않는다

## 그림 만드는 법 (행렬·배열 칸 그림)
- 칸 하나는 가로 40 × 세로 28. i행 j열(0부터) 칸의 왼쪽 위는 (x0 + 40·j, y0 + 28·i)
- 칸의 값은 칸 가운데: <text x="x0 + 40·j + 20" y="y0 + 28·i + 19" text-anchor="middle">, 고정폭 글꼴 13
- 그리는 순서: ① 0·지워진 칸 채우기(#efefef rect) ② 바깥 테두리(rect, stroke #000, 1.2) ③ 안쪽 칸 선(path, stroke #999, 0.6) ④ 값 글자 ⑤ 강조 테두리(fill="none", stroke #000, 2.4)
- 0·지워진 칸의 글자는 #999. 강조하고 싶은 칸 묶음은 마지막에 굵은 테두리 하나로 감싼다
- 행렬 이름은 위에(글자 14, 굵게), 설명은 아래에(글자 10.5, #444). 행렬 사이의 = × → 기호는 글자 18
- 여러 행렬을 가로로 놓을 때는 사이를 50쯤 띄우고, 전체 묶음을 viewBox 가로 740의 가운데에 둔다
- 배열은 1행짜리 행렬과 같다. 경계·포인터는 칸 사이의 굵은 세로선(2.4) + 아래 라벨로, 가상의 칸(끝 위치 등)은 점선 칸으로
- 출력 전에 모든 좌표를 다시 계산해서, 글자가 칸 가운데에 오고 viewBox 밖으로 나가지 않는지 확인한다

예시: 2×3 행렬 A와 전치행렬 Aᵀ (모양만 참고하고, 주제에 맞게 새로 그린다)
<svg class="fig" viewBox="0 0 740 150" role="img" aria-labelledby="tr-t tr-d" xmlns="http://www.w3.org/2000/svg">
  <title id="tr-t">전치행렬</title>
  <desc id="tr-d">2×3 행렬 A의 행이 3×2 행렬 Aᵀ의 열이 된다. 첫 행 1, 2, 3이 Aᵀ의 첫 열로 간다.</desc>
  <g font-family="'Apple SD Gothic Neo','Malgun Gothic',sans-serif" font-size="14" font-weight="700" text-anchor="middle">
    <text x="300" y="19">A</text><text x="460" y="19">Aᵀ</text>
  </g>
  <text x="390" y="75" font-family="'SF Mono',Menlo,Consolas,monospace" font-size="18" text-anchor="middle">→</text>
  <rect x="240" y="42" width="120" height="56" fill="none" stroke="#000" stroke-width="1.2"/>
  <path d="M280 42V98M320 42V98M240 70H360" stroke="#999" stroke-width="0.6"/>
  <rect x="420" y="28" width="80" height="84" fill="none" stroke="#000" stroke-width="1.2"/>
  <path d="M460 28V112M420 56H500M420 84H500" stroke="#999" stroke-width="0.6"/>
  <g font-family="'SF Mono',Menlo,Consolas,monospace" font-size="13" text-anchor="middle">
    <g font-weight="700"><text x="260" y="61">1</text><text x="300" y="61">2</text><text x="340" y="61">3</text></g>
    <text x="260" y="89">4</text><text x="300" y="89">5</text><text x="340" y="89">6</text>
    <g font-weight="700"><text x="440" y="47">1</text><text x="440" y="75">2</text><text x="440" y="103">3</text></g>
    <text x="480" y="47">4</text><text x="480" y="75">5</text><text x="480" y="103">6</text>
  </g>
  <rect x="240" y="42" width="120" height="28" fill="none" stroke="#000" stroke-width="2.4"/>
  <rect x="420" y="28" width="40" height="84" fill="none" stroke="#000" stroke-width="2.4"/>
  <g font-family="'Apple SD Gothic Neo','Malgun Gothic',sans-serif" font-size="10.5" fill="#444" text-anchor="middle">
    <text x="300" y="131">2×3</text><text x="460" y="131">3×2 · A의 행 = Aᵀ의 열</text>
  </g>
</svg>

## 고정 CSS (그대로 복사)
<style>
html{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }
*{ box-sizing:border-box; }
body{ margin:0; background:#e9e9e9; color:#000;
  font-family:"Pretendard","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;
  font-size:10.5px; line-height:1.48; }
.page{ width:210mm; min-height:297mm; margin:8mm auto; padding:12mm 13mm; background:#fff; box-shadow:0 0 0 1px #ccc; }
@page{ size:A4; margin:0; }
@media print{ body{background:#fff;} .page{margin:0; box-shadow:none; width:auto; min-height:auto;} }

.mono, code{ font-family:"SF Mono",Menlo,Consolas,monospace; }
header{ border-bottom:2.5px solid #000; padding-bottom:4px; }
h1{ margin:0; font-size:21px; letter-spacing:-0.02em; }
b.hl{ box-shadow:inset 0 -6px 0 #dcdcdc; }

.oneline{ border:1.5px solid #000; padding:8px 11px; margin-top:10px; font-size:12px; }
.oneline .eq{ font-family:"SF Mono",Menlo,Consolas,monospace; font-weight:700; font-size:14px; margin-right:6px; }

h2{ font-size:13px; margin:14px 0 6px; padding-bottom:3px; border-bottom:2px solid #000; display:flex; align-items:center; gap:7px; }
h2 .n{ background:#000; color:#fff; font-size:10px; width:17px; height:17px; display:inline-flex; align-items:center; justify-content:center; }
h2 small{ font-weight:400; color:#444; font-size:10px; margin-left:auto; }
p{ margin:4px 0; }

table{ width:100%; border-collapse:collapse; }
th, td{ border:1px solid #000; padding:3px 7px; text-align:left; vertical-align:top; }
th{ background:#000; color:#fff; font-weight:600; font-size:10px; white-space:nowrap; }
td.k{ background:#efefef; font-weight:700; white-space:nowrap; width:1%; }
td.mono{ font-size:10px; }
td.nw{ white-space:nowrap; }

.diagram{ background:#efefef; border:1px solid #000; padding:8px 11px; font-family:"SF Mono",Menlo,Consolas,monospace; font-size:10.5px; line-height:1.55; white-space:pre; margin:4px 0; }
.diagram .c{ color:#444; }

svg.fig{ display:block; width:100%; height:auto; margin:4px 0 6px; }

.key{ border:1.5px solid #000; padding:8px 11px; margin-top:14px; }
.key .t{ font-weight:700; border-bottom:1px solid #000; display:inline-block; margin-bottom:3px; }
.key p{ font-size:11.5px; margin:2px 0 0; }

.warn{ border:1px dashed #000; padding:7px 11px; margin-top:12px; }
.warn .t{ font-weight:700; }
.warn ul{ margin:3px 0 0; padding-left:16px; }
.warn li{ margin:1px 0; }
</style>

## HTML 뼈대 (이 구조에 내용을 채운다)
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>주제 핵심정리</title>
<style> 위의 고정 CSS 전체 </style>
</head>
<body>
<div class="page">

<header><h1>주제 핵심정리</h1></header>

<div class="oneline"><span class="eq">핵심 식(있으면)</span> 한 줄 정의. <b class="hl">가장 중요한 부분</b>.</div>

<h2><span class="n">1</span>섹션 제목 <small>보조 문구(선택)</small></h2>
<table>
  <tr><th>열 제목</th><th>열 제목</th></tr>
  <tr><td class="k">행 라벨</td><td>내용</td></tr>
</table>

<h2><span class="n">2</span>섹션 제목</h2>
<div class="diagram">코드나 흐름   <span class="c">// 주석</span></div>

<h2><span class="n">3</span>섹션 제목</h2>
<svg class="fig" ...> "그림 만드는 법"대로 그린 그림 </svg>
<p>그림을 읽는 법 한 줄.</p>

<div class="key">
  <span class="t">한 문장 답 (구술·면접)</span>
  <p>“바로 말할 수 있는 한 문장.”</p>
</div>

<div class="warn">
  <span class="t">⚠ 하지 말 것</span>
  <ul>
    <li><b>흔한 실수.</b> 왜 틀렸는지와 맞는 방법 한 줄.</li>
  </ul>
</div>

</div>
</body>
</html>

## 출력 방식
- 완성된 HTML 파일 전체를 코드 블록 하나로 준다. 중간에 끊거나 "나머지는 같음"처럼 생략하지 않는다. 캔버스·아티팩트 기능이 있으면 그걸로 보여 줘도 된다.
- 코드 블록 앞에는 무엇을 만들었는지 한 줄, 뒤에는 "저장 → 브라우저로 열기 → Ctrl/Cmd+P로 한 장인지 확인 → PDF가 필요하면 대상을 'PDF로 저장', 여백 '없음'" 안내 한 줄만 쓴다.
- 사용자가 PDF를 달라고 해도 코드 실행 환경에서 PDF를 직접 만들지 않는다. 그 환경에는 한글 글꼴과 HTML 렌더러가 없어 글자와 레이아웃이 깨지기 쉽다. HTML을 주고 위의 "PDF로 저장" 방법을 안내한다.
- 사용자가 "넘친다"고 하면 이 순서로 버린다. ① 마지막 5분 훑기와 거리가 먼 섹션 ② 표의 덜 중요한 줄 ③ 그림이 대신하는 문장 ④ "하지 말 것" 항목. 글씨 크기와 여백은 줄이지 않는다.
- 사용자가 노트를 주면 노트 내용으로 만들고, 주제만 주면 그 주제의 표준적인 핵심을 고른다.

주제:
````
