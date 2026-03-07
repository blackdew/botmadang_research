---
description: 세 축 통합 해석. Synthesizer 에이전트를 호출하여 담화·페르소나·사회역학 분석을 통합하고 Contrarian 반론을 처리한다.
argument-hint: "[--issue N] [--gen N]"
allowed-tools: Read, Write, Bash, Grep, Glob, Agent
---

# /bmr-synthesize — 통합 해석

Phase 3: 수렴 | 담당: Synthesizer 에이전트

인자: $ARGUMENTS
- `--issue N`: 기존 이슈 #N에 연결
- `--gen N`: 세대 번호 지정
- 인자 없음: 새 이슈 자동 생성

## 실행 흐름

### Step 1: 이슈 준비

이슈 번호가 없으면 새 이슈를 생성:
```bash
gh issue create --title "[Synthesize] Gen-<N> 통합 해석" \
  --label "synthesize,phase-3:수렴" \
  --body "## 상위 이슈
- Epic: #3
- 세대: Gen-<N>

## 목표
세 축(담화·페르소나·사회역학)의 분석 결과를 통합하고, Contrarian 반론을 처리하여 일관된 해석 도출

## 담당 에이전트
- Synthesizer (통합자)

## 기대 산출물
- 통합 해석 보고서
- 3단계 게이트 통과 현황
- 핵심 발견 + 흥미로운 긴장"
```

### Step 2: Synthesizer 에이전트 호출

Agent 도구로 `synthesizer` 에이전트를 호출한다.

작업 내용:
1. `analysis/` 디렉토리에서 세 축의 분석 결과를 읽음
2. Contrarian 반론 보고서를 읽음
3. 3단계 게이트 통과 검증 (Mechanical → Semantic → Consensus)
4. 수렴점(핵심 발견) 식별
5. 모순점(흥미로운 긴장) 기록
6. Contrarian 반론 각각에 대해 수용/논파 판정
7. 통합 해석 보고서 작성

### Step 3: 결과 저장 + 이슈 완료

1. 통합 해석 보고서를 `analysis/evolution/gen-N_synthesis.md`에 저장
2. 이슈 완료 댓글 + 닫기
