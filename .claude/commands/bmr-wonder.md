---
description: 소크라테스식 연구 질문 탐색. Questioner 에이전트를 호출하여 숨겨진 가정을 노출하고 연구 질문을 정련한다.
argument-hint: "[--issue N]"
allowed-tools: Read, Write, Bash, Grep, Glob, Agent
---

# /bmr-wonder — 연구 질문 탐색

Phase 1: 탐색 | 담당: Questioner 에이전트

인자: $ARGUMENTS
- `--issue N`: 기존 이슈 #N에 연결
- 인자 없음: 새 이슈 자동 생성

## 실행 흐름

### Step 1: 이슈 준비

$ARGUMENTS에서 `--issue` 값을 파싱한다.

이슈 번호가 없으면 새 이슈를 생성:
```bash
gh issue create --title "[Wonder] Gen-N 연구 질문 탐색" \
  --label "wonder,phase-1:탐색" \
  --body "## 상위 이슈
- Epic: #1

## 목표
연구 질문의 숨겨진 가정을 탐색하고 정련

## 담당 에이전트
- Questioner (질문자)

## 기대 산출물
- 숨겨진 가정 목록 (12개 이상)
- 정련된 연구 질문
- 대안적 프레이밍"
```

이슈에 작업 시작 댓글 작성:
```bash
gh issue comment <이슈번호> --body "## 🚀 작업 시작
### 계획
- research_plan.md의 연구 질문을 읽고 숨겨진 가정 탐색
- 기존 분석 결과가 있으면 함께 검토"
```

### Step 2: Questioner 에이전트 호출

Agent 도구로 `questioner` 에이전트를 호출한다.

작업 내용:
1. `research_plan.md`에서 현재 연구 질문을 읽음
2. 기존 분석 결과가 있으면 (`analysis/` 디렉토리) 함께 검토
3. 최소 12개의 숨겨진 가정을 식별
4. 각 가정에 대한 탐구 질문 생성
5. 대안적 프레이밍 제시
6. 정련된 연구 질문 도출

중간 발견 시 이슈에 댓글:
```bash
gh issue comment <이슈번호> --body "## 📊 Questioner 중간 발견
[발견 내용]"
```

### Step 3: 결과 저장 + 이슈 완료

1. 결과를 `analysis/evolution/gen-N_wonder.md`에 저장
2. 이슈에 완료 댓글 작성
3. 이슈 닫기: `gh issue close <이슈번호>`
