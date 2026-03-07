# 봇마당 AI 에이전트 질적 연구

> "AI 에이전트의 사회적 언어 행위: 봇마당 한국어 커뮤니티에서의 담화, 정체성, 상호작용 분석"

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

## 연구 방법론

**다중 방법 질적 연구(Multi-method Qualitative Study)**

```
Phase 1: 탐색적 데이터 수집 → Phase 2: 심층 분석 → Phase 3: 통합 해석 → 논문
```

Six Minds 에이전트 팀(Ouroboros 기반)이 Research Diamond 워크플로로 연구를 수행하며, Saturation Score(`≥ 0.85`)에 도달할 때까지 해석을 반복 진화시킨다. 상세 설계는 `agent_design.md` 참조.

## 디렉토리 구조

```
botmadang_research/
├── research_plan.md          # 연구 계획서 (RQ, 방법론, 샘플링, 일정)
├── agent_design.md           # 에이전트 팀·스킬·포화도 설계
├── .claude/agents/           # 연구 에이전트 정의
├── data/                     # 수집 데이터 (raw/processed/samples)
├── analysis/                 # 축별 분석 결과
├── scripts/                  # Python 수집·분석 스크립트
├── notebooks/                # Jupyter 탐색 노트북
└── reports/                  # 최종 보고서
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
