---
description: 포화도 계산 + 수렴 판정. Synthesizer 에이전트를 포화도 평가 모드로 호출하여 Saturation Score를 계산한다.
argument-hint: "[--issue N] [--gen N]"
allowed-tools: Read, Write, Bash, Grep, Glob, Agent
---

# /bmr-saturate — 포화도 계산

Phase 3: 수렴 | 담당: Synthesizer 에이전트 (포화도 평가 모드)

인자: $ARGUMENTS
- `--issue N`: 기존 이슈 #N에 연결
- `--gen N`: 세대 번호 지정
- 인자 없음: 새 이슈 자동 생성

## 실행 흐름

### Step 1: 이슈 준비

이슈 번호가 없으면 새 이슈를 생성:
```bash
gh issue create --title "[Saturate] Gen-<N> 포화도 평가" \
  --label "saturate,phase-3:수렴" \
  --body "## 상위 이슈
- Epic: #3
- 세대: Gen-<N>

## 목표
Saturation Score 계산 및 수렴 판정

## 담당 에이전트
- Synthesizer (통합자) — 포화도 평가 모드

## 기대 산출물
- Saturation Score + 차원별 점수
- 수렴 판정 (포화/부분 포화/미포화)
- 다음 행동 권고"
```

### Step 2: Synthesizer 에이전트 (포화도 모드) 호출

Agent 도구로 `synthesizer` 에이전트를 포화도 평가 모드로 호출한다.

Saturation Score 계산:
```
차원              가중치   기준
코드 포화          30%    새 테마 등장 빈도
주제 안정성        25%    추가 데이터의 주제 변경 여부
축 간 삼각검증     25%    세 축 분석 수렴 정도
반론 해소          20%    주요 반론 수용/논파 여부
```

판정 기준:
- ≥ 0.85: "포화 도달" → 분석 종료, 논문 작성
- 0.65~0.84: "부분 포화" → 특정 축 추가 분석
- < 0.65: "미포화" → 수집 및 분석 계속

### Step 3: 결과 출력 + 이슈 완료

대시보드 형태로 출력:
```
┌──────────────────────────────────┐
│     Saturation Score: 0.765      │
│     판정: 부분 포화               │
├──────────────────────────────────┤
│ 코드 포화     ████████░░  0.90   │
│ 주제 안정성   ████████░░  0.80   │
│ 삼각검증     ███████░░░  0.70   │
│ 반론 해소     ██████░░░░  0.60   │
├──────────────────────────────────┤
│ 권고: ...                        │
└──────────────────────────────────┘
```

1. 결과를 `analysis/evolution/gen-N_saturation.md`에 저장
2. 이슈 완료 댓글 + 닫기
