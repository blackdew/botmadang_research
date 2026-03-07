---
description: 연구 보고서 생성. Synthesizer 에이전트를 보고서 모드로 호출하여 통합 해석 결과를 학술 보고서 형태로 작성한다.
argument-hint: "[--issue N] [--format <형식>]"
allowed-tools: Read, Write, Bash, Grep, Glob, Agent
---

# /bmr-report — 연구 보고서 생성

유틸리티 | 담당: Synthesizer 에이전트 (보고서 모드)

인자: $ARGUMENTS
- `--issue N`: 기존 이슈 #N에 연결
- `--format <형식>`: 보고서 형식 (full, summary, executive)
- 인자 없음: 새 이슈 자동 생성 + full 보고서

## 실행 흐름

### Step 1: 이슈 준비

이슈 번호가 없으면 새 이슈를 생성:
```bash
gh issue create --title "[Report] 연구 보고서 생성" \
  --label "synthesize" \
  --body "## 목표
통합 해석 결과를 학술 보고서 형태로 작성

## 담당 에이전트
- Synthesizer (통합자) — 보고서 모드

## 기대 산출물
- reports/ 디렉토리에 마크다운 보고서"
```

### Step 2: Synthesizer 에이전트 (보고서 모드) 호출

Agent 도구로 `synthesizer` 에이전트를 보고서 모드로 호출한다.

보고서 구조:
1. **Executive Summary** (1페이지)
2. **연구 배경 및 목적**
3. **방법론**
4. **축별 상세 분석**
   - 담화 분석 결과
   - 페르소나 분석 결과
   - 사회적 역학 분석 결과
5. **통합 해석 및 논의**
   - 수렴점 (핵심 발견)
   - 긴장점 (모순과 해석)
   - Contrarian 반론 처리
6. **방법론적 한계**
7. **후속 연구 제안**
8. **부록**: Saturation Score 이력, 세대별 진화 기록

입력: `analysis/` 디렉토리의 모든 결과 + `analysis/evolution/` 세대 기록

### Step 3: 결과 저장 + 이슈 완료

1. 보고서를 `reports/YYYY-MM-DD_research_report.md`에 저장
2. 이슈 완료 댓글 + 닫기
