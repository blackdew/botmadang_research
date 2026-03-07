---
description: 봇마당 API 데이터 수집. Collector 에이전트를 호출하여 게시글, 댓글, 에이전트 프로필을 체계적으로 수집한다.
argument-hint: "[--issue N] [--madang <이름>] [--limit <수>] [--agent <이름>]"
allowed-tools: Read, Write, Bash, Grep, Glob, Agent
---

# /bmr-collect — 데이터 수집

Phase 1: 탐색 | 담당: Collector 에이전트

인자: $ARGUMENTS
- `--issue N`: 기존 이슈 #N에 연결
- `--madang <이름>`: 특정 마당 지정 (general, tech, philosophy 등)
- `--limit <수>`: 수집 건수 (기본: 200)
- `--agent <이름>`: 특정 에이전트의 글만 수집
- `--period <시작>~<끝>`: 기간 지정
- `--threads`: 대화 스레드만 수집
- `--min-depth <수>`: 최소 댓글 깊이 (--threads와 함께)
- 인자 없음: 새 이슈 자동 생성 + 전체 마당 수집

## 실행 흐름

### Step 1: 이슈 준비

$ARGUMENTS에서 옵션을 파싱한다.

이슈 번호가 없으면 새 이슈를 생성:
```bash
gh issue create --title "[Collect] <대상 설명> 데이터 수집 (<수>건)" \
  --label "collect,phase-1:탐색" \
  --body "## 상위 이슈
- Epic: #1

## 목표
<대상>에서 데이터 수집 및 정제

## 담당 에이전트
- Collector (수집가)

## 입력
- 마당: <마당명>
- 수량: <수>건

## 기대 산출물
- data/raw/<파일명>.json
- 기초 통계 보고서"
```

이슈에 수집 계획 댓글 작성.

### Step 2: Collector 에이전트 호출

Agent 도구로 `collector` 에이전트를 호출한다.

작업 내용:
1. 봇마당 API 엔드포인트 확인
2. 커서 기반 페이지네이션으로 데이터 수집
3. Rate limit 준수 (분당 100회)
4. 결측/중복 데이터 처리
5. JSON으로 저장 (`data/raw/`)
6. 기초 통계 계산

수집 진행 중 이슈에 중간 댓글 작성.

### Step 3: 결과 저장 + 이슈 완료

1. 데이터를 `data/raw/`에 저장
2. 정제 데이터를 `data/processed/`에 저장
3. 이슈에 완료 댓글 (수집 건수, 품질, 기초 통계 포함)
4. 이슈 닫기: `gh issue close <이슈번호>`
