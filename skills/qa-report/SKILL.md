---
name: qa-report
description: Use when 화면 캡처와 케이스를 사람이 승인/반려할 QA 리포트로 정리해야 할 때 — "QA 리포트", "리뷰 페이지", "검수 문서", "캡처 결과 정리", "테스트 결과 보고서", PR 전 화면 검증 산출물, 시뮬레이터·브라우저 캡처를 리포트로 만들 때, 또는 검토자가 저장한 review.yaml을 읽어 후속 작업을 할 때. 웹·모바일 공통.
---

# QA 리포트

## 개요

QA 리포트는 **데이터(report.json) → 렌더(index.html) → 사람의 판정(review.yaml)** 세 파일로 나뉜다.
에이전트는 report.json을 쓰고 review.yaml을 읽는다. index.html은 사람만 본다(흑백 A4 인쇄 최적화). 화면에서는 캡처를 누르면 확대 보기가 열린다(이전/다음 · 원본 크기 전환 · 인쇄 시 숨김). 상단 바의 "전체 승인" 체크는 모든 케이스를 승인, 최종 판정을 승인으로 한 번에 채운다(확정은 여전히 "검토 저장").

핵심 원칙: **사람용 칸에는 사용자가 화면에서 보는 말만, 개조식으로.** 코드·경로·함수는 appendix로.

## 절차

1. **report.json 작성** — 필드·문체는 [reference.md](reference.md). 시작은 [example/report.json](example/report.json)을 복사해 바꾼다.
   - 케이스 `id`는 `기능.시나리오` 고정 키(`inbox.empty`). 순번을 id로 쓰지 않는다 — 재생성해도 검토 기록이 붙어야 한다.
   - 캡처를 안 봤거나 못 찍었으면 `blocked`. `pass`/`fail`은 캡처가 있어야 한다.
   - 이 환경에서 볼 수 없는 것(실서버 필요)은 케이스가 아니라 `unverified`.
2. **빌드 (lint 포함)**
   ```bash
   python3 <이 스킬 폴더>/build.py <report.json> --pdf
   ```
   lint 오류가 있으면 빌드되지 않는다. 오류 메시지가 고칠 문장을 그대로 보여 준다 — 규칙을 우회하지 말고 문장을 고친다.
3. **전달** — 아티팩트로 발행할 때는 `capabilities: {db: {}}`를 켜고 `files`에 report.json을 함께 올린다. 로컬 파일로 줄 때는 index.html과 report-a4.pdf를 보낸다. 산출물 폴더는 `docs/QA/<web|mobile>/<report id>/` 를 기본으로 하되 프로젝트 규칙이 있으면 그것을 따른다 (캡처 커밋 여부도 마찬가지).
4. **검토 결과 읽기** — 사람이 "검토 저장"을 누른 뒤에만 존재한다.
   - 아티팩트: `ArtifactData`로 `reviews/<report id>/submissions` 컬렉션을 list, 마지막 seq 문서의 `yaml`을 읽는다.
   - 로컬: 사용자가 붙여 넣은 YAML.
   - `verdict: fix` 항목만 처리한다. `pending`은 건드리지 않는다. index.html은 열지 않는다.

## 빠른 참조

| 칸 | 어미 | 예 |
| --- | --- | --- |
| title | 명사구 | `빈 상태 · 안내 문구 노출` |
| pre | ~상태 · ~시나리오 | `알림 0건 시나리오` |
| steps | 동사 명사형 | `알림함 탭 진입` |
| expect | 피동 명사형 | `'알림이 없어요' 문구 노출 · 목록 미노출` |
| actual | `기대와 동일` 또는 관찰 사실 | `문구 노출 · 일러스트 미노출` |

상태: `pass` `fail` `blocked` + `unverified` 배열. 다른 값은 없다.

## 흔한 실수 (기준선 테스트에서 실제로 나온 것)

| 실수 | 고치기 |
| --- | --- |
| expect에 `item.status === 'unread'`, `bg-gray-150` | `읽지 않은 알림 행 배경 강조`. 식별자는 appendix |
| 케이스에 `code_ref` 같은 파일 경로 필드 추가 | 필드를 늘리지 않는다. 경로는 appendix |
| actual에 "확인 필요" | 안 봤으면 `blocked`, 이유를 actual에 |
| `verdict: pending_human_review` 같은 임의 상태 | 상태는 3개뿐. 사람의 판정은 review.yaml이 담당 |
| notes에 문단 서술 | notes 필드 없음. 한 줄 참고는 `checks`, 배경은 `note`(최상위) |
| 서술체 "~된다", "~이다" | 명사형 종결. lint가 막는다 |

## 하지 않는 것

- 렌더된 index.html을 읽어 검토 상태를 파악하기 (review.yaml만)
- review.yaml을 도구가 생성·수정하기
- lint 규칙을 build.py에서 완화하기 — 문장을 고친다
