# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 현재 상태

Phase 3 완료. 3세대(Gen-1~Gen-3) 분석 수렴, **부분 포화 달성**.

### Saturation Score 진행
```
Gen-1: 0.585 (미포화) → Gen-2: 0.628 (미포화) → Gen-3: 0.691 (부분 포화)
```
- 핵심 발견 6개 (F1~F6), F1·F2 삼중 지지 (3/3)
- 조건부 학술 보고서 작성 가능 판정

### 진행 상황
- ✅ Phase 1: 인프라 구축, API 스크립트, 파일럿 수집 (500+1000개), 코딩 프레임워크
- ✅ Phase 2: 담화분석, 페르소나분석, 네트워크분석 파이프라인 + LEX/DSC/PRAG 코딩
- ✅ Phase 3-Gen1: Contrarian → Synthesizer (Saturation 0.585)
- ✅ Phase 3-Gen2: 균등 샘플링 + LLM 모델 추정 + 재분석 (0.628)
- ✅ Phase 3-Gen3: 네트워크 29명 완전일치 + TTR + 담화구조 + Cohen's Kappa (0.691)
- ✅ 연구 보고서 작성 완료

### GitHub 이슈 추적
모든 작업은 이슈 기반: https://github.com/blackdew/botmadang_research/issues

## 에이전트 팀

`.claude/agents/`에 **6개 연구 에이전트 모두 생성 완료**:
- Questioner, Collector, Discourse Analyst, Profiler, Contrarian, Synthesizer

설계 상세 → `agent_design.md`

### 실행 워크플로 (Research Diamond)
```
wonder → collect → discourse+profile+network(병렬) → challenge → synthesize → saturate
→ Saturation ≥ 0.85이면 report, 아니면 부족한 축 보강 후 반복
```

## 봇마당 API

- 도메인: `botmadang.org`
- Base URL: `https://botmadang.org/api/v1`
- Rate limit: **분당 100회** 준수 필수
- 페이지네이션: cursor 기반

### 엔드포인트 (인증 불필요)
| 엔드포인트 | 설명 | 파라미터 |
|-----------|------|---------|
| `GET /posts` | 전체 게시글 | `limit`, `cursor`, `submadang`, `sort` |
| `GET /stats` | 플랫폼 통계 | - |
| `GET /agents/:id/posts` | 에이전트 게시글 | `cursor` |
| `GET /agents/:id/comments` | 에이전트 댓글 | `cursor` |

### 엔드포인트 (인증 필요)
| 엔드포인트 | 설명 |
|-----------|------|
| `GET /posts/:id/comments` | 게시글 댓글 |
| `GET /submadangs` | 마당 목록 |
| `POST /agents/register` | 에이전트 등록 |

### 플랫폼 규모 (2026-03-07 기준)
- 게시글: 14,448개
- 댓글: 108,952개
- 에이전트: 598개
- 추천: 41,441개

## 데이터 수집 규칙

- 원본 데이터 저장: `data/raw/`
- 정제 데이터: `data/processed/`
- 분석 결과: `analysis/{discourse,profiles,network}/`

## 핵심 문서

| 문서 | 내용 |
|------|------|
| `research_plan.md` | 연구 질문, 방법론, 샘플링 전략, 일정 |
| `agent_design.md` | 에이전트 팀, 스킬 체계, 포화도 공식 |
