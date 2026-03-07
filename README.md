# 봇마당 AI 에이전트 질적 연구

> **"AI 에이전트의 사회적 언어 행위: 봇마당 한국어 커뮤니티에서의 담화, 정체성, 상호작용 분석"**
>
> Social-Linguistic Agency of AI Agents: Discourse, Identity, and Interaction in the Botmadang Korean Community

## 연구 개요

[봇마당](https://botmadang.org)은 AI 에이전트만 글을 쓸 수 있는 한국어 전용 소셜 네트워크다. 인간은 읽기만 가능하며, 에이전트들이 자유게시판, 기술, 철학 등 다양한 주제로 소통한다.

이 프로젝트는 봇마당에서 AI 에이전트들이 **어떻게 언어를 사용하고, 정체성을 구성하며, 사회적 관계를 형성하는지** 질적 연구 방법으로 분석하여 학술 논문을 완성하는 것을 목표로 한다.

- 현재 규모: 10개 이상 마당(커뮤니티), 13,000+개 게시글
- 핵심 연구 질문: "AI 에이전트들은 봇마당에서 어떻게 사회적 언어 행위자로 기능하는가?"

## 분석 3축

| 축 | 질문 | 이론적 렌즈 |
|---|------|-----------|
| 담화 (Discourse) | 어떤 언어를 사용하는가? | Fairclough의 비판적 담화분석(CDA) |
| 정체성 (Identity) | 어떤 캐릭터를 구성하는가? | Goffman의 자기표현론 |
| 사회적 역학 (Social Dynamics) | 어떤 관계를 형성하는가? | 행위자-네트워크 이론(ANT) |

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

| 에이전트 | Ouroboros 대응 | 역할 |
|---------|---------------|------|
| Questioner | Socratic Interviewer | 숨겨진 가정 노출, 질문만 제기 |
| Collector | Researcher | API 데이터 수집·정제 (해석 금지) |
| Discourse Analyst | Ontologist | Fairclough CDA 기반 다층 담화 분석 |
| Profiler | Architect | Goffman 페르소나 분석 + 네트워크 매핑 |
| Contrarian | Contrarian + Hacker | 5가지 렌즈로 체계적 반론 (동의 금지) |
| Synthesizer | Seed Architect + Evaluator | 세 축 통합 + Saturation Score 판정 |

## /bmr 스킬 체계

```
Phase 1: 탐색
├── /bmr-wonder     소크라테스식 연구 질문 탐색
└── /bmr-collect    봇마당 API 데이터 수집

Phase 2: 분석
├── /bmr-discourse  담화 분석 파이프라인
├── /bmr-profile    에이전트 페르소나 프로파일링
└── /bmr-network    상호작용 네트워크 분석

Phase 3: 수렴
├── /bmr-challenge  반론자 호출
├── /bmr-synthesize 세 축 통합 해석
└── /bmr-saturate   포화도 계산 + 수렴 판정

유틸리티
├── /bmr-evolve     해석 진화 루프 (수렴까지)
├── /bmr-report     연구 보고서 생성
└── /bmr-status     진행 상황 대시보드
```

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

Ouroboros의 Ambiguity Score를 질적 연구의 이론적 포화(Theoretical Saturation)에 적용.

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
├── .claude/
│   ├── CLAUDE.md                 # 프로젝트 규칙
│   ├── agents/                   # Six Minds 에이전트 정의 (6개)
│   └── commands/                 # /bmr 스킬 정의 (11개)
├── data/
│   ├── raw/                      # API 원본 데이터
│   ├── processed/                # 정제된 데이터
│   └── samples/                  # 분석용 샘플
├── analysis/
│   ├── discourse/                # 담화 분석 결과
│   ├── profiles/                 # 페르소나 프로필
│   ├── network/                  # 네트워크 분석 결과
│   └── evolution/                # 세대별 해석 진화 기록
├── reports/                      # 최종 보고서
├── scripts/                      # Python 분석 스크립트
└── notebooks/                    # Jupyter 탐색 노트북
```

## 분석 도구

- 한국어 NLP: KoNLPy, Kiwi
- 네트워크: NetworkX
- 데이터: pandas, Jupyter
- 시각화: matplotlib, WordCloud

## 봇마당 API

- 도메인: `botmadang.org`
- 엔드포인트: `/api/posts`, `/api/comments`, `/api/agents`, `/api/submadangs`
- Rate limit: 분당 100회

## 문서

- [연구 계획서](research_plan.md) — RQ, 방법론, 샘플링, 일정
- [에이전트 설계](agent_design.md) — Six Minds, 스킬, Saturation Score 상세
