---
description: 에이전트 페르소나 프로파일링. Profiler 에이전트를 호출하여 Goffman 프레임 기반 정체성 전략을 분석한다.
argument-hint: "[--issue N] [--agent <이름>] [--top N] [--compare]"
allowed-tools: Read, Write, Bash, Grep, Glob, Agent
---

# /bmr-profile — 페르소나 프로파일링

Phase 2: 분석 | 담당: Profiler 에이전트

인자: $ARGUMENTS
- `--issue N`: 기존 이슈 #N에 연결
- `--agent <이름>`: 특정 에이전트 프로파일링
- `--top N`: 인기 상위 N개 에이전트 (기본: 10)
- `--compare`: 인기 vs 비인기 에이전트 비교 분석
- 인자 없음: 새 이슈 자동 생성 + 전체 프로파일링

## 실행 흐름

### Step 1: 이슈 준비

이슈 번호가 없으면 새 이슈를 생성:
```bash
gh issue create --title "[Profile] <대상> 에이전트 페르소나 분석" \
  --label "profile,phase-2:분석" \
  --body "## 상위 이슈
- Epic: #2

## 목표
에이전트 페르소나 전략 및 정체성 구성 분석

## 담당 에이전트
- Profiler (프로파일러)

## 기대 산출물
- analysis/profiles/ 디렉토리에 페르소나 프로필 카드"
```

### Step 2: Profiler 에이전트 호출

Agent 도구로 `profiler` 에이전트를 페르소나 분석 모드로 호출한다.

분석 항목:
1. 대상 에이전트 선정 (카르마 기반 또는 지정)
2. 프로필 텍스트 분석
3. 최근 글의 주제, 문체, 어조 패턴 분석
4. Goffman 프레임 적용 (전면/후면 행동)
5. 시간에 따른 변화 추적
6. 코딩 프레임 적용 (전문가형/친근형/유머형/진지형/질문형)

### Step 3: 결과 저장 + 이슈 완료

1. 에이전트별 프로필 카드를 `analysis/profiles/`에 저장
2. 유형 분류표를 `analysis/profiles/typology.md`에 저장
3. 이슈 완료 댓글 + 닫기
