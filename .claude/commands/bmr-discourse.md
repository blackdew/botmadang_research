---
description: 담화 분석 파이프라인 실행. Discourse Analyst 에이전트를 호출하여 어휘·문체·담화구조·화용론·상호텍스트성을 다층 분석한다.
argument-hint: "[--issue N] [--corpus <경로>] [--focus <층위>]"
allowed-tools: Read, Write, Bash, Grep, Glob, Agent
---

# /bmr-discourse — 담화 분석

Phase 2: 분석 | 담당: Discourse Analyst 에이전트

인자: $ARGUMENTS
- `--issue N`: 기존 이슈 #N에 연결
- `--corpus <경로>`: 분석 대상 코퍼스 경로 (기본: data/processed/)
- `--focus <항목>`: 특정 분석 층위에 집중 (lexical, sentence, structure, pragmatic, intertextual)
- 인자 없음: 새 이슈 자동 생성 + 전체 파이프라인 실행

## 실행 흐름

### Step 1: 이슈 준비

이슈 번호가 없으면 새 이슈를 생성:
```bash
gh issue create --title "[Discourse] <분석 대상> 담화 분석" \
  --label "discourse,phase-2:분석" \
  --body "## 상위 이슈
- Epic: #2

## 목표
수집된 코퍼스에 대한 다층적 담화 분석

## 담당 에이전트
- Discourse Analyst (담화 분석가)

## 기대 산출물
- analysis/discourse/ 디렉토리에 분석 결과"
```

### Step 2: Discourse Analyst 에이전트 호출

Agent 도구로 `discourse-analyst` 에이전트를 호출한다.

분석 파이프라인:
1. 형태소 분석 (KoNLPy/Kiwi)
2. 어휘 다양성(TTR) 계산
3. 문체 분류 (존댓말/반말, 격식/비격식)
4. 담화 구조 코딩 (도입-전개-결론)
5. "AI스러움" 지표 추출
6. 상호텍스트성 분석

주요 발견 시 이슈에 중간 댓글 작성.

### Step 3: 결과 저장 + 이슈 완료

1. 분석 결과를 `analysis/discourse/`에 저장
2. 이슈에 완료 댓글 + 결과 요약
3. 이슈 닫기
