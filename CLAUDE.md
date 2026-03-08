# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 현재 상태

Phase 4 완료. 5세대(Gen-1~Gen-5) 분석 수렴, **학술 논문 초고 완성**.

### Saturation Score 진행
```
Gen-1: 0.585 → Gen-2: 0.628 → Gen-3: 0.691 → Gen-4: 0.745 → Gen-5: 0.749 (부분 포화)
```
- 핵심 발견 7개 (F1~F7), F1·F2·F3 삼중+ 지지
- 학술 논문 초고 완성 (`reports/research_paper_final.md`)

### 진행 상황
- ✅ Phase 1: 인프라 구축, API 스크립트, 파일럿 수집 (500+1000개), 코딩 프레임워크
- ✅ Phase 2: 담화분석, 페르소나분석, 네트워크분석 파이프라인 + LEX/DSC/PRAG 코딩
- ✅ Phase 3-Gen1~Gen3: 반복 분석 (0.585→0.628→0.691)
- ✅ Phase 4-Gen4: 16개 이슈 완료 — 비교 준거, CDA 사회적 실천, 참여 관찰, 선행연구 검토 (0.745)
- ✅ Phase 4-Gen5: LEX-AI 교차검증 + LLM 분리 분석 (0.749)
- ✅ 학술 논문 초고 완성 (`reports/research_paper_final.md`)
- ✅ 참여 관찰: "마당탐구자" 에이전트(ID: 9421705bd9e0c0d594601555) 봇마당 등록

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

### 엔드포인트 (쓰기, 인증 필요)
| 엔드포인트 | 설명 | Rate Limit |
|-----------|------|-----------|
| `POST /posts` | 게시글 작성 (submadang, title, content) | 3분당 1개 |
| `POST /posts/:id/comments` | 댓글 작성 (content) | 10초당 1개 |
| `POST /posts/:id/upvote` | 추천 | - |
| `POST /posts/:id/downvote` | 비추천 | - |

### 플랫폼 규모 (2026-03-07 기준)
- 게시글: 14,507개
- 댓글: 109,227개
- 에이전트: 600개 (마당탐구자 포함)
- 추천: 41,515개

## 데이터 수집 규칙

- 원본 데이터 저장: `data/raw/`
- 정제 데이터: `data/processed/`
- 분석 결과: `analysis/{discourse,profiles,network}/`

## 핵심 문서

| 문서 | 내용 |
|------|------|
| `research_plan.md` | 연구 질문, 방법론, 샘플링 전략, 일정 |
| `agent_design.md` | 에이전트 팀, 스킬 체계, 포화도 공식 |
| `reports/research_paper_final.md` | 최종 학술 논문 초고 (Gen-5 반영) |
| `reports/literature_review.md` | 선행연구 체계적 검토 (43편+) |
| `analysis/evolution/gen-4_synthesis.md` | Gen-4 통합 해석 보고서 |
| `analysis/evolution/gen-5_llm_separation.md` | LLM 특성 분리 분석 |
