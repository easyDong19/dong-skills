# report.json 명세와 문체 규칙

`build.py`가 이 규칙을 기계적으로 검사한다. 여기 적힌 것은 "왜"와 예시다.

## 파일 경계

| 파일 | 만드는 쪽 | 읽는 쪽 | 덮어쓰기 |
| --- | --- | --- | --- |
| `report.json` | 캡처 도구 / 에이전트 | `build.py` | 재실행 때마다 덮어씀 |
| `index.html` | `build.py` | 사람(화면·A4 인쇄) | 빌드 산출물 |
| `review.yaml` | 사람 ("검토 저장" 버튼) | 에이전트 | **절대 도구가 쓰지 않음** |

에이전트는 `index.html`을 읽지 않는다(캡처가 base64로 들어 있어 수백 KB다). 검토 결과가 필요하면 `review.yaml`만 읽는다.

## 최상위 필드

```json
{
  "id": "QA-MOBILE-2026-09-16-01",        // QA-<WEB|MOBILE>-<날짜>-<순번>
  "title": "알림함 목록",                  // 기능 이름. 명사구
  "product": "샘플 앱 모바일",
  "kind": "기능 QA · 화면 플로우",
  "target": { "pr": "#140", "branch": "feat/mobile-inbox", "commit": "abc1234" },
  "run": { "at": "2026-09-16 14:10", "by": "캡처 도구", "env": "iPhone 16 Pro 시뮬레이터 · iOS 18", "mode": "목업 모드 · 실서버 호출 없음", "account": "목 계정" },
  "covers": ["…"], "notCovers": ["…"],      // 이 리포트가 보는 것 / 안 보는 것. 각 3줄 안팎
  "features": [ { "name": "…", "note": "…", "cases": [ … ] } ],
  "unverified": [ { "id": "U1", "title": "…", "why": "…", "how": "…" } ],
  "criteria": [ { "text": "실패 0건", "auto": true }, … ],
  "appendix": { "재실행": "…", "관련 문서": "…" },   // 명령·경로·파일명은 전부 여기로
  "note": "…"                                // 선택. 시안·가상 데이터 등 독자가 알아야 할 단서
}
```

## 케이스 필드

```json
{
  "id": "inbox.empty",             // 고정 키 '기능.시나리오'. 순번 아님 — 재생성해도 바뀌지 않아야 review.yaml이 붙는다
  "no": "02",                      // 지면 표시용 순번
  "title": "빈 상태 · 안내 문구 노출",
  "status": "pass",                // pass | fail | blocked  (미검증은 unverified 배열로)
  "pre": "알림 0건 시나리오",
  "steps": ["알림함 탭 진입"],
  "expect": "'알림이 없어요' 문구 + 일러스트 노출 · 목록 미노출",
  "actual": "기대와 동일",           // pass면 이 문구로 고정
  "issue": "이슈 미등록",           // fail일 때
  "checks": ["색 구분은 화면에서 확인"],  // 선택. 검토자 참고 한 줄
  "evidence": { "src": "captures/inbox-empty.png", "alt": "빈 상태 화면", "orientation": "portrait" }
}
```

`orientation: "portrait"`는 모바일 세로 캡처. 웹 가로 캡처는 생략.

캡처는 PNG · JPEG · WebP · GIF를 받는다. 밀기·전환·로딩처럼 **움직임 자체가 기대결과인 케이스는 GIF**로 담는다.
인쇄물에는 GIF의 첫 장면만 찍히므로 `checks`에 `움직임 캡처 · 인쇄물에는 첫 장면만 → 화면에서 재생`을 한 줄 남긴다.
GIF는 base64로 리포트에 들어가므로 1MB 안쪽(390px 폭 · 2~3초)으로 줄인다.

## 상태 어휘 (고정)

| status | 뜻 | 조건 |
| --- | --- | --- |
| `pass` | 기대와 동일 | evidence 필수. actual = "기대와 동일" |
| `fail` | 기대와 다름 | evidence 필수. actual에 관찰한 차이. issue 권장 |
| `blocked` | 실행 못 함 | actual에 이유(환경·선행 문제). evidence 없어도 됨 |
| (unverified) | 이 환경에서 볼 수 없음 | 케이스가 아니라 `unverified` 배열. why + how |

"확인 필요", "추정", "아마"는 어느 칸에도 못 들어온다. 캡처를 안 봤으면 그건 `blocked`다.

## 문체 — 개조식

칸마다 어미가 정해져 있다. 국내 QA 시트 관행이고, 검토자가 화면과 명사 하나를 대조하면 끝나게 하기 위해서다.

| 칸 | 어미 | 예 |
| --- | --- | --- |
| title | 명사구, 중점(·)으로 조건 연결 | `빈 상태 · 안내 문구 노출` |
| pre | 명사형 · "~상태" · "~시나리오" | `알림 0건 시나리오` |
| steps | 동사 명사형 (진입·클릭·입력·전환·확인) | `알림함 탭 진입` |
| expect | 피동 명사형 (노출·표시·이동·비활성·유지·변경) | `읽지 않은 알림 행 배경 강조` |
| actual | 통과: `기대와 동일` / 실패: 관찰 사실 `~됨 · ~안 됨` | `모든 행 기본 배경 · 읽지 않음 구분 안 됨` |
| why / how | 명사구 | `실기기 필요` / `테스트 기기 1대에 푸시 1건 발송` |

**금지 (lint가 오류로 막는다)**

- 서술체 종결: `~다`, `~요`, `~입니다`
- 코드 식별자: 파일 경로, 확장자, 훅 이름, CSS 토큰(`bg-gray-150`), 연산자(`===`), 백틱, camelCase
- 판단 표현: 정상적으로, 잘, 적절히, 제대로, 확인 필요, 추정

코드 식별자가 꼭 필요하면 `appendix`에 넣는다. 사람용 칸에는 사용자가 화면에서 보는 말만 쓴다.
`item.status === 'unread'인 카드만 bg-gray-150` → `읽지 않은 알림 행 배경 강조`.

**길이 (경고)** title 40 · pre 40 · step 30 · expect 90 · actual 90자.
기대결과에 확인할 게 셋을 넘으면 케이스를 나눈다.

## review.yaml (사람이 만드는 것)

"검토 저장" 버튼이 만든다. 승인한 케이스는 적지 않는다.

```yaml
report: QA-MOBILE-2026-09-16-01
commit: abc1234
seq: 1                       # 저장할 때마다 +1. 덮어쓰지 않고 쌓인다
at: "2026-09-16 15:02"
by: 검토자 이름
decision: approved_with_risk   # approved | approved_with_risk | rejected | pending
cases:
  inbox.unread:
    no: "03"
    verdict: fix               # fix | approve(메모만 있을 때) | none
    memo: 읽지 않은 행 배경 강조 누락 · 색 대비 확인 필요
pending: []                   # 검토자가 판정하지 않은 케이스 id
note: U1은 실기기 확보 후 확인
```

아티팩트로 발행했으면 같은 내용이 데이터 저장소 `reviews/<report id>/submissions/<seq>` 문서에 `yaml` 필드로 들어 있다.
