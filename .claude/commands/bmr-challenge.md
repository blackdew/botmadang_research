---
description: 반론자(Contrarian) 호출. 현재 분석 결과에 5가지 렌즈(방법론·이론·기술·대안·범위)로 체계적 반론을 제기한다.
argument-hint: "[--issue N] [--target <경로>] [--axis <축>] [--gen N]"
allowed-tools: Read, Write, Bash, Grep, Glob, Agent
---

# /bmr-challenge — 반론 호출

Phase 3: 수렴 | 담당: Contrarian 에이전트

인자: $ARGUMENTS
- `--issue N`: 기존 이슈 #N에 연결
- `--target <경로>`: 반론 대상 분석 결과 경로
- `--axis <축>`: 특정 축에 집중 (discourse, identity, social)
- `--gen N`: 세대 번호 지정
- 인자 없음: 새 이슈 자동 생성 + 전체 분석 결과에 대해 반론

## 실행 흐름

### Step 1: 이슈 준비

이슈 번호가 없으면 새 이슈를 생성:
```bash
gh issue create --title "[Challenge] Gen-<N> 분석 결과 반론" \
  --label "challenge,phase-3:수렴" \
  --body "## 상위 이슈
- Epic: #3
- 세대: Gen-<N>

## 목표
현재 분석 결과에 대한 체계적 반론 제기

## 담당 에이전트
- Contrarian (반론자)

## 기대 산출물
- 반론 보고서 (5가지 렌즈)"
```

### Step 2: Contrarian 에이전트 호출

Agent 도구로 `contrarian` 에이전트를 호출한다.

작업 내용:
1. `analysis/` 디렉토리에서 현재까지의 분석 결과를 모두 읽음
2. 5가지 반론 렌즈 적용 (방법론, 이론, 기술, 대안, 범위)
3. 각 반론에 심각도(높음/중간/낮음) 부여
4. 종합 평가 작성

### Step 3: 결과 저장 + 이슈 완료

1. 반론 보고서를 `analysis/evolution/gen-N_challenge.md`에 저장
2. 이슈 완료 댓글 + 닫기
