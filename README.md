# dong-skills

Claude Code용 스킬 모음입니다. 기술 문서를 쓰고 다듬는 파이프라인, 팀 공유용 작업 메모, QA 리포트, 학습 자료 생성을 다룹니다. 모든 스킬은 한국어 기준으로 작성되어 있습니다.

## 설치

플러그인 세 개로 나뉘어 있습니다. 필요한 것만 설치합니다.

| 플러그인 | 스킬 | 의존성 |
| --- | --- | --- |
| `dong-skills` | 문서 작성 4종 · `daily-scrum` · `qa-report` | 없음 |
| `dong-study` | `study-explainer` · `a4-study-sheet` | [diagram-design](https://github.com/cathrynlavery/diagram-design) (자동 설치) |
| `dong-all` | 위 두 플러그인을 한 번에 | 위와 같음 |

```bash
claude plugin marketplace add easydong19/dong-skills
claude plugin install dong-skills@dong-skills
```

`dong-study`나 `dong-all`을 설치하려면 diagram-design 마켓플레이스를 **먼저** 추가합니다. Claude Code는 다른 마켓플레이스를 대신 추가해 주지 않으므로, 이 단계를 빼면 `Is the "diagram-design" marketplace added?` 오류로 설치가 멈춥니다.

```bash
claude plugin marketplace add cathrynlavery/diagram-design
claude plugin install dong-study@dong-skills
```

diagram-design은 `dong-study`의 의존성으로 함께 설치됩니다. `a4-study-sheet`가 A4 요약에 그림을 넣을 때 이 스킬의 원칙을 불러 씁니다.

설치하면 스킬은 `<플러그인>:<스킬 이름>`(예: `dong-skills:qa-report`, `dong-study:a4-study-sheet`)으로 불립니다. 대화 중 요청 내용이 스킬 설명과 맞으면 Claude가 자동으로 고릅니다.

플러그인을 쓰지 않으려면 레포를 클론해 `skills/` 아래 폴더를 `~/.claude/skills/` 에 복사해도 됩니다. 이때 diagram-design은 직접 설치합니다.

## 스킬 목록

스킬별 시나리오 · 호출 예시 · 결과 이미지는 [docs/](docs/README.md)에 있습니다.

### 기술 문서 작성 파이프라인

네 스킬이 "유형 결정 → 구조 리뷰 → 문장 윤문" 순서로 역할을 나눕니다. 설명형 본문은 별도 스킬이 담당합니다.

| 스킬 | 언제 | 무엇을 |
| --- | --- | --- |
| [`choosing-doc-type`](docs/skills/choosing-doc-type.md) | 문서를 쓰기 시작하기 전 | Diátaxis 4유형(학습·문제 해결·참조·설명) 중 하나를 2축 결정표로 정한다. 한 문서 = 한 유형 |
| [`doc-structure-review`](docs/skills/doc-structure-review.md) | 초안·목차가 나온 뒤 | 5개 정보 구조 원칙으로 진단하고 통합 개선 목차 하나를 낸다 |
| [`doc-sentence-polish`](docs/skills/doc-sentence-polish.md) | 문장을 다듬을 때 | 6개 원칙으로 문장 수준 피드백과 통합 수정안을 낸다. 의미는 바꾸지 않는다 |
| [`explaining-with-domain-context`](docs/skills/explaining-with-domain-context.md) | 코드·플로우·결정을 설명할 때 | 문제와 도메인부터 시작해 인과 사슬로 서술한다. 인수인계·온보딩 문서에도 쓴다 |

### 작업 공유

| 스킬 | 무엇을 |
| --- | --- |
| [`daily-scrum`](docs/skills/daily-scrum.md) | 그날의 커밋·PR을 비개발자도 읽을 수 있는 기능 단위 스크럼 메모로 만든다. 스크럼 테이블 셀에 바로 붙일 평문 형식 |
| [`qa-report`](docs/skills/qa-report.md) | 화면 캡처와 케이스를 `report.json` 으로 정리하고 `build.py` 로 사람이 승인·반려할 A4 인쇄용 리포트를 만든다. 캡처 확대 보기와 전체 승인을 지원하고, 개조식 문체를 lint로 강제한다 |

### 학습 자료 (`dong-study`)

| 스킬 | 무엇을 |
| --- | --- |
| [`study-explainer`](docs/skills/study-explainer.md) | 개념을 처음 보는 사람도 이해할 수 있게 배경·비유·그림을 채운 학습용 HTML |
| [`a4-study-sheet`](docs/skills/a4-study-sheet.md) | 시험·면접 직전에 들고 볼 흑백 A4 1장 인쇄용 요약본. 그림은 diagram-design 원칙으로 흑백 인라인 SVG로 그린다 |

**Claude Code 없이 쓰기:** ChatGPT나 Claude 채팅에서는 [`chat/a4-study-sheet.md`](chat/a4-study-sheet.md)의 지시문을 복사해 붙여 넣고 주제만 쓰면 됩니다.

## 구조

```
skills/<스킬 이름>/SKILL.md   스킬 본문 (frontmatter의 description이 트리거 조건)
skills/qa-report/build.py     report.json → index.html 빌더 (표준 라이브러리만 사용)
skills/qa-report/example/     샘플 report.json과 가상 알림함 캡처 (PNG · GIF)
chat/a4-study-sheet.md        ChatGPT·Claude 채팅에 붙여 넣는 a4-study-sheet 지시문
docs/                         스킬별 사용 예시와 결과 이미지
scripts/capture-docs.py       docs 예시 이미지 재생성 (playwright)
.claude-plugin/marketplace.json   마켓플레이스 · 플러그인 정의 (dong-skills · dong-study · dong-all)
plugins/dong-all/             묶음 플러그인 (스킬 없이 의존성만)
```

## 라이선스

MIT
