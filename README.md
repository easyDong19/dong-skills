# dong-skills

Claude Code용 스킬 모음입니다. 기술 문서를 쓰고 다듬는 파이프라인, 팀 공유용 작업 메모, QA 리포트, 학습 자료 생성을 다룹니다. 모든 스킬은 한국어 기준으로 작성되어 있습니다.

## 설치

Claude Code 플러그인 마켓플레이스로 설치합니다.

```bash
claude plugin marketplace add easydong19/dong-skills
claude plugin install dong-skills@dong-skills
```

설치하면 스킬은 `dong-skills:<스킬 이름>` 으로 불립니다. 대화 중 요청 내용이 스킬 설명과 맞으면 Claude가 자동으로 고릅니다.

플러그인을 쓰지 않으려면 레포를 클론해 `skills/` 아래 폴더를 `~/.claude/skills/` 에 복사해도 됩니다.

## 스킬 목록

### 기술 문서 작성 파이프라인

네 스킬이 "유형 결정 → 구조 리뷰 → 문장 윤문" 순서로 역할을 나눕니다. 설명형 본문은 별도 스킬이 담당합니다.

| 스킬 | 언제 | 무엇을 |
| --- | --- | --- |
| `choosing-doc-type` | 문서를 쓰기 시작하기 전 | Diátaxis 4유형(학습·문제 해결·참조·설명) 중 하나를 2축 결정표로 정한다. 한 문서 = 한 유형 |
| `doc-structure-review` | 초안·목차가 나온 뒤 | 5개 정보 구조 원칙으로 진단하고 통합 개선 목차 하나를 낸다 |
| `doc-sentence-polish` | 문장을 다듬을 때 | 5개 원칙으로 문장 수준 피드백과 통합 수정안을 낸다. 의미는 바꾸지 않는다 |
| `explaining-with-domain-context` | 코드·플로우·결정을 설명할 때 | 문제와 도메인부터 시작해 인과 사슬로 서술한다. 인수인계·온보딩 문서에도 쓴다 |

### 작업 공유

| 스킬 | 무엇을 |
| --- | --- |
| `daily-scrum` | 그날의 커밋·PR을 비개발자도 읽을 수 있는 기능 단위 스크럼 메모로 만든다. 스크럼 테이블 셀에 바로 붙일 평문 형식 |
| `qa-report` | 화면 캡처와 케이스를 `report.json` 으로 정리하고 `build.py` 로 사람이 승인·반려할 A4 인쇄용 리포트를 만든다. 개조식 문체를 lint로 강제한다 |

### 학습 자료

| 스킬 | 무엇을 |
| --- | --- |
| `study-explainer` | 개념을 처음 보는 사람도 이해할 수 있게 배경·비유·그림을 채운 학습용 HTML |
| `a4-study-sheet` | 시험·면접 직전에 들고 볼 흑백 A4 1장 인쇄용 요약본 |

## 구조

```
skills/<스킬 이름>/SKILL.md   스킬 본문 (frontmatter의 description이 트리거 조건)
skills/qa-report/build.py     report.json → index.html 빌더 (표준 라이브러리만 사용)
skills/qa-report/example/     샘플 report.json과 자리표시 캡처
.claude-plugin/               플러그인·마켓플레이스 매니페스트
```

## 라이선스

MIT
