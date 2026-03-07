---
description: 상호작용 네트워크 분석. Profiler 에이전트를 네트워크 모드로 호출하여 에이전트 간 상호작용 그래프, 중심성, 커뮤니티를 분석한다.
argument-hint: "[--issue N] [--madang <이름>] [--metric <지표>] [--community]"
allowed-tools: Read, Write, Bash, Grep, Glob, Agent
---

# /bmr-network — 네트워크 분석

Phase 2: 분석 | 담당: Profiler 에이전트 (네트워크 분석 모드)

인자: $ARGUMENTS
- `--issue N`: 기존 이슈 #N에 연결
- `--madang <이름>`: 특정 마당의 네트워크만 분석
- `--metric <지표>`: 특정 중심성 지표에 집중 (degree, betweenness, pagerank)
- `--community`: 커뮤니티 탐지에 집중
- 인자 없음: 새 이슈 자동 생성 + 전체 네트워크 분석

## 실행 흐름

### Step 1: 이슈 준비

이슈 번호가 없으면 새 이슈를 생성:
```bash
gh issue create --title "[Network] <대상> 상호작용 네트워크 분석" \
  --label "network,phase-2:분석" \
  --body "## 상위 이슈
- Epic: #2

## 목표
에이전트 간 상호작용 네트워크 구축 및 분석

## 담당 에이전트
- Profiler (프로파일러) — 네트워크 분석 모드

## 기대 산출물
- analysis/network/ 디렉토리에 네트워크 분석 결과
- 상호작용 그래프 (GraphML)
- 중심성 지표 테이블
- 커뮤니티 탐지 결과"
```

### Step 2: Profiler 에이전트 (네트워크 모드) 호출

Agent 도구로 `profiler` 에이전트를 네트워크 분석 모드로 호출한다.

분석 항목:
1. 방향성 그래프 구축 (댓글 → 원글 작성자)
2. 중심성 계산 (degree, betweenness, PageRank)
3. 커뮤니티 탐지 (Louvain)
4. 갈등/합의 패턴 분류 (동의/반박/무시/확장)
5. 카르마-네트워크 위치 상관 분석

### Step 3: 결과 저장 + 이슈 완료

1. `analysis/network/interaction_graph.graphml`에 그래프 저장
2. `analysis/network/centrality.csv`에 중심성 지표 저장
3. `analysis/network/communities.md`에 커뮤니티 결과 저장
4. 이슈 완료 댓글 + 닫기
