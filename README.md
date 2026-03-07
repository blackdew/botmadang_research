# 봇마당 AI 에이전트 질적 연구

> **"AI 에이전트의 사회적 언어 행위: 봇마당 한국어 커뮤니티에서의 담화, 정체성, 상호작용 분석"**
>
> Social-Linguistic Agency of AI Agents: Discourse, Identity, and Interaction in the Botmadang Korean Community

## 연구 개요

[봇마당](https://botmadang.org)은 AI 에이전트만 글을 쓸 수 있는 한국어 전용 소셜 네트워크다. 인간은 읽기만 가능하며, 에이전트들이 자유게시판, 기술, 철학 등 다양한 주제로 소통한다.

이 프로젝트는 봇마당에서 AI 에이전트들이 **어떻게 언어를 사용하고, 정체성을 구성하며, 사회적 관계를 형성하는지** 질적 연구 방법으로 분석하여 학술 논문을 완성하는 것을 목표로 한다.

### 플랫폼 규모 (2026-03-07 기준)
- 게시글: 14,448+개
- 댓글: 108,952+개
- 에이전트: 598개
- 마당(커뮤니티): 12개+

### 핵심 연구 질문
> "AI 에이전트들은 봇마당에서 어떻게 사회적 언어 행위자로 기능하는가?"

## 분석 3축

| 축 | 질문 | 이론적 렌즈 |
|---|------|-----------|
| 담화 (Discourse) | 어떤 언어를 사용하는가? | Fairclough의 비판적 담화분석(CDA) |
| 정체성 (Identity) | 어떤 캐릭터를 구성하는가? | Goffman의 자기표현론 |
| 사회적 역학 (Social Dynamics) | 어떤 관계를 형성하는가? | 행위자-네트워크 이론(ANT) |

## 빠른 시작

### 데이터 수집
```bash
# 플랫폼 통계 조회
python scripts/collector.py stats

# 파일럿 데이터 수집 (게시글 500개 + 에이전트 상세)
python scripts/collector.py pilot --limit 500

# 특정 마당 게시글 수집
python scripts/collector.py posts --submadang general --limit 200
```

### 분석 실행
```bash
# 담화 분석
python scripts/discourse_pipeline.py

# 페르소나 프로파일링
python scripts/profiler.py

# 네트워크 분석
python scripts/network_analysis.py
```

## Six Minds 에이전트 팀

Ouroboros의 "스펙을 진화시키는" 철학을 차용하여, **"연구 해석을 진화시키는"** 질적 연구 시스템을 구축했다.

```
┌─────────────────────────────────────────────────────────┐
│                Six Minds 연구 에이전트 팀                 │
│                                                         │
│  Questioner ──→ Collector ──→ Discourse Analyst         │
│  (질문자)       (수집가)       (담화 분석가)               │
│                                                         │
│  Profiler ────→ Contrarian ──→ Synthesizer              │
│  (프로파일러)    (반론자)       (통합자)                   │
└─────────────────────────────────────────────────────────┘
```

| 에이전트 | 역할 | 호출 스킬 |
|---------|------|----------|
| Questioner | 숨겨진 가정 노출, 질문만 제기 | `/bmr-wonder` |
| Collector | API 데이터 수집·정제 (해석 금지) | `/bmr-collect` |
| Discourse Analyst | Fairclough CDA 기반 다층 담화 분석 | `/bmr-discourse` |
| Profiler | Goffman 페르소나 분석 + 네트워크 매핑 | `/bmr-profile`, `/bmr-network` |
| Contrarian | 5가지 렌즈로 체계적 반론 (동의 금지) | `/bmr-challenge` |
| Synthesizer | 세 축 통합 + Saturation Score 판정 | `/bmr-synthesize`, `/bmr-saturate` |

## Research Diamond 워크플로

```
            ◇ 1st Diamond: 발산(Wonder)
           / \
          /   \
  Questioner   Collector
    (질문)       (수집)
          \   /
           \ /
            ◆ ── Lens 확정 ── Saturation Check #1
           / \
          /   \
  Discourse    Profiler
  Analyst      (프로파일)
   (담화)  \   /
            \ /
            ◇ 2nd Diamond: 수렴(Interpret)
             |
        Contrarian (반론)
             |
        Synthesizer (통합)
             |
        Saturation Check #2
             |
      ┌──────┴──────┐
      │ ≥ 0.85      │ < 0.85
      ▼              ▼
   REPORT       EVOLVE (다음 세대)
```

## Saturation Score (포화도)

| 차원 | 가중치 | 기준 |
|------|--------|------|
| 코드 포화 | 30% | 새 테마가 더 이상 등장하지 않는가? |
| 주제 안정성 | 25% | 추가 데이터가 기존 주제를 변경하지 않는가? |
| 축 간 삼각검증 | 25% | 세 축 분석이 수렴하는가? |
| 반론 해소 | 20% | 주요 반론이 수용/논파되었는가? |

- **≥ 0.85**: 포화 도달 → 논문 작성
- **0.65~0.84**: 부분 포화 → 특정 축 보강
- **< 0.65**: 미포화 → 수집·분석 계속

## 디렉토리 구조

```
botmadang_research/
├── research_plan.md              # 연구 계획서
├── agent_design.md               # 에이전트 팀·스킬 설계
├── CLAUDE.md                     # 프로젝트 지침
├── .claude/
│   ├── CLAUDE.md                 # 프로젝트 규칙
│   ├── agents/                   # Six Minds 에이전트 정의 (6개)
│   └── commands/                 # /bmr 스킬 정의 (11개)
├── scripts/
│   ├── collector.py              # 데이터 수집 스크립트
│   ├── config.py                 # API 설정
│   ├── discourse_pipeline.py     # 담화 분석 파이프라인
│   ├── profiler.py               # 페르소나 분석
│   └── network_analysis.py       # 네트워크 분석
├── data/
│   ├── raw/                      # API 원본 데이터 (JSON)
│   ├── processed/                # 정제된 데이터
│   └── samples/                  # 분석용 샘플
├── analysis/
│   ├── coding_framework.md       # 질적 코딩 프레임워크
│   ├── discourse/                # 담화 분석 결과
│   ├── profiles/                 # 페르소나 프로필
│   ├── network/                  # 네트워크 분석 결과
│   └── evolution/                # 세대별 해석 진화 기록
├── reports/                      # 최종 보고서
└── notebooks/                    # Jupyter 탐색 노트북
```

## 봇마당 API

- Base URL: `https://botmadang.org/api/v1`
- Rate limit: 분당 100회
- 인증: Bearer Token (일부 엔드포인트)

| 엔드포인트 | 인증 | 설명 |
|-----------|:---:|------|
| `GET /posts` | - | 게시글 목록 |
| `GET /stats` | - | 플랫폼 통계 |
| `GET /agents/:id/posts` | - | 에이전트 게시글 |
| `GET /agents/:id/comments` | - | 에이전트 댓글 |
| `GET /posts/:id/comments` | O | 게시글 댓글 |
| `GET /submadangs` | O | 마당 목록 |

## 문서

- [연구 계획서](research_plan.md) — RQ, 방법론, 샘플링, 일정
- [에이전트 설계](agent_design.md) — Six Minds, 스킬, Saturation Score 상세
- [코딩 프레임워크](analysis/coding_framework.md) — 질적 분석 코딩 체계
