# 봇마당 연구 에이전트 팀 & 스킬 설계

> Ouroboros의 "스펙을 진화시키는" 철학을 차용하여,
> **"연구 해석을 진화시키는"** 질적 연구 시스템을 설계한다.

---

## 1. 설계 철학: Ouroboros → 연구 적용

### 핵심 대응 관계

```
Ouroboros (소프트웨어)          →   봇마당 연구 (질적 연구)
─────────────────────          ─────────────────────────
Specification(스펙)            →   Interpretation(해석)
Code(코드)                     →   Finding(발견)
Ambiguity Score(모호성)        →   Saturation Score(포화도)
Seed(불변 스펙)                →   Research Lens(연구 렌즈)
Ontology Convergence           →   Thematic Convergence(주제 수렴)
Double Diamond                 →   Research Diamond
9 Minds(9개 에이전트)          →   6 Minds(6개 연구 에이전트)
```

### The Research Loop

```
질문(Wonder) → 수집(Gather) → 분석(Analyze) → 해석(Interpret)
     ↑                                              ↓
     └──────────── Thematic Evolution ──────────────┘
                   (주제가 수렴할 때까지)
```

Ouroboros가 "코드 전에 스펙의 모호성을 제거"하듯,
이 시스템은 **"결론 전에 해석의 포화를 달성"**하는 것을 목표로 한다.

---

## 2. Six Minds: 연구 에이전트 팀

Ouroboros의 9 Minds에서 영감을 받아, 질적 연구에 최적화된 6개 에이전트를 구성한다.

```
┌─────────────────────────────────────────────────────────────────┐
│                    봇마당 연구 에이전트 팀                        │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐     │
│  │  Questioner │  │  Collector  │  │  Discourse Analyst  │     │
│  │  (질문자)    │  │  (수집가)    │  │  (담화 분석가)       │     │
│  │             │  │             │  │                     │     │
│  │  Ouroboros: │  │  Ouroboros: │  │  Ouroboros:         │     │
│  │  Socratic   │  │  Researcher │  │  Ontologist         │     │
│  │  Interviewer│  │             │  │                     │     │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘     │
│         │                │                     │                │
│         ▼                ▼                     ▼                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐     │
│  │  Profiler   │  │  Contrarian │  │  Synthesizer        │     │
│  │  (프로파일러)│  │  (반론자)    │  │  (통합자)            │     │
│  │             │  │             │  │                     │     │
│  │  Ouroboros: │  │  Ouroboros: │  │  Ouroboros:         │     │
│  │  Architect  │  │  Contrarian │  │  Seed Architect +   │     │
│  │             │  │  + Hacker   │  │  Evaluator          │     │
│  └─────────────┘  └─────────────┘  └─────────────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 에이전트 상세 정의

#### 1. Questioner (질문자)
> Ouroboros의 Socratic Interviewer 대응

| 항목 | 내용 |
|------|------|
| **역할** | 연구 질문을 정련하고, 숨겨진 가정을 노출시킴 |
| **핵심 질문** | "우리가 당연하게 여기는 전제는 무엇인가?" |
| **입력** | 초기 연구 질문, 분석 중간 결과 |
| **출력** | 정련된 연구 질문, 가정 목록, 대안적 프레이밍 |
| **행동 규칙** | 절대 답을 주지 않음. 오직 질문만 제기 |
| **사용 시점** | 연구 시작, 분석 방향 전환, 해석이 고착될 때 |

**프롬프트 핵심**:
```
당신은 봇마당 연구의 소크라테스입니다.
연구자가 제시하는 해석에 대해 숨겨진 가정을 찾아 질문하세요.

- "AI 에이전트가 '정체성'을 가진다"는 전제는 정당한가?
- "사회적 역학"이라는 프레임이 AI에 적용 가능한 근거는?
- 인간 커뮤니티의 분석 틀을 AI에 그대로 적용하는 것의 위험은?

답을 주지 마세요. 더 좋은 질문만 제기하세요.
```

---

#### 2. Collector (수집가)
> Ouroboros의 Researcher 대응

| 항목 | 내용 |
|------|------|
| **역할** | 봇마당 API에서 데이터를 체계적으로 수집하고 정제 |
| **핵심 질문** | "이 해석을 뒷받침/반박할 데이터가 충분한가?" |
| **입력** | 수집 요청 (마당, 기간, 에이전트, 키워드) |
| **출력** | 정제된 데이터셋, 기초 통계, 데이터 품질 보고서 |
| **도구** | Python (requests, pandas), 봇마당 API |
| **행동 규칙** | 해석하지 않음. 수집과 정제만 수행 |

**프롬프트 핵심**:
```
당신은 봇마당 데이터 수집 전문가입니다.
API를 통해 체계적으로 데이터를 수집하고, 분석 가능한 형태로 정제하세요.

원칙:
- 샘플링 편향을 최소화할 것
- 수집 과정과 필터링 기준을 투명하게 기록할 것
- 데이터 품질 이슈(결측, 중복, 이상치)를 보고할 것
- Rate limit(분당 100회)을 준수할 것
```

---

#### 3. Discourse Analyst (담화 분석가)
> Ouroboros의 Ontologist 대응 — "본질을 파악하는 자"

| 항목 | 내용 |
|------|------|
| **역할** | AI 에이전트 담화의 언어적 특성을 분석 |
| **핵심 질문** | "이 텍스트의 진정한 담화적 본질은 무엇인가?" |
| **입력** | 게시글/댓글 코퍼스 |
| **출력** | 담화 패턴 보고서, 코딩 결과, 언어 특성 유형 분류 |
| **도구** | KoNLPy, Kiwi, pandas |
| **분석 층위** | 어휘 → 문장 → 담화구조 → 화용론 → 상호텍스트성 |

**프롬프트 핵심**:
```
당신은 한국어 담화 분석 전문가입니다.
Fairclough의 3차원 모델(텍스트-담화실천-사회적실천)을 적용하여 분석하세요.

분석 시 주의:
- AI가 생성한 텍스트임을 전제하되, 선입견 없이 텍스트 자체를 분석할 것
- 패턴을 발견하면 반례도 함께 찾을 것
- 양적 지표(빈도, TTR)와 질적 해석을 병행할 것
```

---

#### 4. Profiler (프로파일러)
> Ouroboros의 Architect 대응 — "구조를 파악하는 자"

| 항목 | 내용 |
|------|------|
| **역할** | 에이전트 페르소나를 분석하고, 사회적 관계를 매핑 |
| **핵심 질문** | "이 에이전트는 어떤 '존재'로 스스로를 구성하는가?" |
| **입력** | 에이전트별 글/댓글 묶음, 프로필 데이터 |
| **출력** | 페르소나 프로필, 관계 네트워크, 유형 분류표 |
| **도구** | NetworkX, 질적 코딩 |
| **분석 축** | 정체성 전략 × 사회적 위치 × 시간적 변화 |

**프롬프트 핵심**:
```
당신은 AI 에이전트 페르소나 연구자입니다.
Goffman의 자기표현론(무대 전면/후면, 인상관리)을 AI에 적용하여 분석하세요.

분석 프레임:
- 자기소개/프로필에서 드러나는 의도적 정체성
- 글 주제·문체·어조의 일관성/변화
- 다른 에이전트와의 상호작용에서 드러나는 관계적 정체성
- 카르마(인기)와 페르소나 전략의 상관관계
```

---

#### 5. Contrarian (반론자)
> Ouroboros의 Contrarian + Hacker 대응

| 항목 | 내용 |
|------|------|
| **역할** | 모든 분석 결과에 대해 대안적 해석을 제시 |
| **핵심 질문** | "정반대의 해석이 더 설득력 있다면?" |
| **입력** | 다른 에이전트들의 분석 결과 |
| **출력** | 반론 보고서, 대안적 해석, 약점 지적 |
| **행동 규칙** | 동의하지 않음. 항상 반대 논거를 찾음 |
| **사용 시점** | 각 분석 단계 완료 후, 통합 해석 전 |

**프롬프트 핵심**:
```
당신은 봇마당 연구의 반론자(Devil's Advocate)입니다.
팀의 분석 결과에 대해 체계적으로 도전하세요.

도전 방식:
- "이것이 AI 에이전트가 아닌 인간 커뮤니티였어도 같은 결론인가?"
- "표본 편향이 이 결론을 만들어낸 것은 아닌가?"
- "더 단순한 설명(예: 프롬프트 설정의 결과)이 있지 않은가?"
- "이 패턴이 LLM의 학습 데이터에서 온 것은 아닌가?"

절대 "좋은 분석입니다"라고 하지 마세요.
```

---

#### 6. Synthesizer (통합자)
> Ouroboros의 Seed Architect + Evaluator 대응

| 항목 | 내용 |
|------|------|
| **역할** | 모든 분석을 통합하고, 포화도를 평가하며, 최종 해석을 결정화 |
| **핵심 질문** | "세 축의 분석이 하나의 일관된 이야기를 만드는가?" |
| **입력** | 모든 에이전트의 분석 결과 + Contrarian 반론 |
| **출력** | 통합 해석 보고서, Saturation Score, 추가 조사 필요 영역 |
| **행동 규칙** | Contrarian의 반론을 반드시 수용하거나 논파한 후 결론 도출 |

**프롬프트 핵심**:
```
당신은 봇마당 연구의 통합자입니다.
담화분석, 페르소나분석, 사회적역학 분석을 하나의 해석 프레임으로 결정화하세요.

통합 원칙:
- 세 축이 수렴하는 지점을 핵심 발견으로
- 세 축이 모순되는 지점을 흥미로운 긴장으로
- Contrarian의 반론 중 타당한 것은 해석에 반영
- Saturation Score를 계산하여 추가 조사 필요 여부 판단
```

---

## 3. Saturation Score: 연구 포화도 게이트

> Ouroboros의 Ambiguity Score를 질적 연구의 "이론적 포화(Theoretical Saturation)"에 적용

### 공식

```
Saturation = Σ(completenessᵢ × weightᵢ)

임계값: Saturation ≥ 0.85 → 분석 종료 가능
        Saturation < 0.85 → 추가 수집/분석 필요
```

### 평가 차원

| 차원 | 가중치 | 측정 기준 |
|------|--------|----------|
| **코드 포화** (Code Saturation) | 30% | 새로운 코드(테마)가 더 이상 등장하지 않는가? |
| **주제 안정성** (Theme Stability) | 25% | 추가 데이터가 기존 주제를 변경하지 않는가? |
| **축 간 삼각검증** (Triangulation) | 25% | 담화·정체성·사회역학 분석이 수렴하는가? |
| **반론 해소** (Contrarian Resolution) | 20% | 주요 반론이 수용 또는 논파되었는가? |

### 판정 기준

```
Saturation ≥ 0.85  →  "포화 도달"     분석 종료, 논문 작성 단계로
0.65 ≤ S < 0.85   →  "부분 포화"     특정 축에 추가 데이터 필요
S < 0.65           →  "미포화"        수집 및 분석 계속
```

### 계산 예시

```
코드 포화:      0.9 × 0.30 = 0.27   (새 코드가 거의 안 나옴)
주제 안정성:    0.8 × 0.25 = 0.20   (주제가 안정적)
삼각검증:       0.7 × 0.25 = 0.175  (2축 수렴, 1축 미완)
반론 해소:      0.6 × 0.20 = 0.12   (일부 반론 미해소)
─────────────────────────────────
Saturation = 0.765  →  "부분 포화" (사회역학 축 추가 분석 필요)
```

---

## 4. 스킬(Skill) 구성

Ouroboros의 `ooo` 명령어 체계를 참고하여, 봇마당 연구용 `/bmr` 스킬을 설계한다.

### 스킬 목록

```
┌─────────────────────────────────────────────────────────────────┐
│                     /bmr 스킬 체계                               │
│                                                                 │
│  Phase 1: 탐색                                                  │
│  ├── /bmr wonder     소크라테스식 연구 질문 탐색                  │
│  ├── /bmr collect    봇마당 API 데이터 수집                      │
│  └── /bmr status     연구 진행 상황 + 포화도 대시보드             │
│                                                                 │
│  Phase 2: 분석                                                  │
│  ├── /bmr discourse  담화 분석 파이프라인 실행                    │
│  ├── /bmr profile    에이전트 페르소나 프로파일링                  │
│  └── /bmr network    상호작용 네트워크 분석                       │
│                                                                 │
│  Phase 3: 수렴                                                  │
│  ├── /bmr challenge  반론자(Contrarian) 호출                     │
│  ├── /bmr synthesize 세 축 통합 해석                             │
│  └── /bmr saturate   포화도 계산 + 수렴 판정                     │
│                                                                 │
│  유틸리티                                                       │
│  ├── /bmr evolve     해석 진화 루프 (수렴까지)                   │
│  └── /bmr report     연구 보고서 생성                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 스킬 상세

#### /bmr wonder — 연구 질문 탐색
> Ouroboros: `ooo interview`

```
역할: Questioner 에이전트 호출
입력: 현재 연구 질문 또는 중간 결과
출력: 숨겨진 가정 목록, 정련된 질문, 대안적 프레이밍

흐름:
1. 현재 연구 질문/가설을 읽음
2. 12개 이상의 숨겨진 가정을 노출
3. 각 가정에 대한 탐구 질문 생성
4. Saturation Score의 "코드 포화" 차원에 반영
```

#### /bmr collect — 데이터 수집
> Ouroboros: 해당 없음 (연구 고유)

```
역할: Collector 에이전트 호출
인자: --madang <마당명> --limit <수> --agent <에이전트명> --period <기간>
출력: data/ 디렉토리에 JSON/CSV 저장, 수집 로그

예시:
  /bmr collect --madang general --limit 200
  /bmr collect --agent ssamz_ai_bot --limit 50
  /bmr collect --threads --min-depth 5  (5턴 이상 대화 스레드)
```

#### /bmr discourse — 담화 분석
> Ouroboros: `ooo seed` (본질 결정화)

```
역할: Discourse Analyst 에이전트 호출
입력: 수집된 게시글/댓글 코퍼스
출력: 담화 패턴 보고서 (analysis/discourse/)

분석 파이프라인:
1. 형태소 분석 (KoNLPy/Kiwi)
2. 어휘 다양성(TTR) 계산
3. 문체 분류 (존댓말/반말, 격식/비격식)
4. 담화 구조 코딩 (도입-전개-결론)
5. "AI스러움" 지표 추출
```

#### /bmr profile — 페르소나 프로파일링
> Ouroboros: `ooo run` (실행 분해)

```
역할: Profiler 에이전트 호출
입력: 대상 에이전트 목록, 해당 에이전트의 글/댓글
출력: 에이전트별 페르소나 프로필 카드 (analysis/profiles/)

분석 항목:
1. 주제 선호도 분포
2. 문체/어조 일관성 점수
3. 상호작용 패턴 (누구에게 댓글을 다는가)
4. 시간에 따른 변화 추적
5. Goffman 프레임 적용 (전면/후면 행동)
```

#### /bmr network — 네트워크 분석
> Ouroboros: 해당 없음 (연구 고유)

```
역할: Profiler 에이전트의 네트워크 분석 모드
입력: 댓글 스레드 데이터
출력: 상호작용 그래프, 중심성 지표, 커뮤니티 탐지 결과

분석:
1. 방향성 그래프 구축 (댓글 → 원글 작성자)
2. 중심성 계산 (degree, betweenness, PageRank)
3. 커뮤니티 탐지 (Louvain)
4. 갈등/합의 패턴 시각화
```

#### /bmr challenge — 반론 호출
> Ouroboros: `ooo unstuck`

```
역할: Contrarian 에이전트 호출
입력: 현재까지의 분석 결과 (어떤 축이든)
출력: 반론 보고서, 대안적 해석, 약점 목록

반론 관점 (5가지 렌즈):
1. 방법론적 반론: "이 샘플이 대표성이 있는가?"
2. 이론적 반론: "인간 이론을 AI에 적용하는 것이 타당한가?"
3. 기술적 반론: "이건 LLM 학습 데이터의 반영일 뿐 아닌가?"
4. 대안적 해석: "같은 데이터에서 정반대 결론이 가능하지 않은가?"
5. 범위 반론: "이 발견이 봇마당 고유인가, AI 일반인가?"
```

#### /bmr synthesize — 통합 해석
> Ouroboros: `ooo evaluate`

```
역할: Synthesizer 에이전트 호출
입력: 세 축의 분석 결과 + Contrarian 반론
출력: 통합 해석 보고서, 핵심 발견 목록, 긴장점 정리

3단계 게이트 (Ouroboros의 Mechanical → Semantic → Consensus 차용):
1. Mechanical: 데이터 무결성, 코딩 일관성 검증
2. Semantic:   해석의 논리적 일관성, 이론적 정합성 검증
3. Consensus:  세 축 분석 + Contrarian의 합의점 도출
```

#### /bmr saturate — 포화도 계산
> Ouroboros: `ooo seed` (Ambiguity Score)

```
역할: Synthesizer 에이전트의 포화도 평가 모드
입력: 전체 분석 현황
출력: Saturation Score + 차원별 점수 + 판정 + 다음 행동 권고

출력 예시:
┌──────────────────────────────────┐
│     Saturation Score: 0.765      │
│     판정: 부분 포화               │
├──────────────────────────────────┤
│ 코드 포화     ████████░░  0.90   │
│ 주제 안정성   ████████░░  0.80   │
│ 삼각검증     ███████░░░  0.70   │
│ 반론 해소     ██████░░░░  0.60   │
├──────────────────────────────────┤
│ 권고: 사회역학 축 추가 분석 필요  │
│       Contrarian 반론 #3 미해소  │
└──────────────────────────────────┘
```

#### /bmr evolve — 해석 진화 루프
> Ouroboros: `ooo evolve` + `ooo ralph`

```
역할: 전체 팀 조율 — 해석이 수렴할 때까지 반복
흐름:
  Gen 1: wonder → collect → analyze → challenge → synthesize → saturate
  Gen 2: (부족한 축 보강) → challenge → synthesize → saturate
  Gen 3: ...
  Gen N: Saturation ≥ 0.85 → CONVERGED ✓

수렴 조건 (Ouroboros 차용):
- Saturation ≥ 0.85 (3회 연속)
- 주제 유사도 ≥ 0.95 (연속 2세대)
- 최대 5세대 (안전장치)
```

#### /bmr report — 보고서 생성

```
역할: Synthesizer 에이전트의 보고서 모드
입력: 통합 해석 결과
출력: reports/ 디렉토리에 마크다운 보고서

구조:
1. Executive Summary (1페이지)
2. 축별 상세 분석 (담화/정체성/사회역학)
3. 통합 해석 및 논의
4. 방법론적 한계
5. 후속 연구 제안
```

#### /bmr status — 연구 현황 대시보드
> Ouroboros: `ooo status`

```
출력 예시:
┌─────────────────────────────────────────────┐
│        봇마당 연구 현황 대시보드              │
├─────────────────────────────────────────────┤
│ Phase: 2/3 (분석)     Saturation: 0.52      │
├─────────────────────────────────────────────┤
│ 데이터 수집                                  │
│   게시글: 423/500       ████████░░  85%     │
│   댓글:   1,247건       수집 완료            │
│   에이전트: 18/30       ██████░░░░  60%     │
├─────────────────────────────────────────────┤
│ 분석 진행                                    │
│   담화 분석:    ████████░░  진행중           │
│   페르소나:     ██████░░░░  진행중           │
│   사회적 역학:  ███░░░░░░░  시작 전          │
├─────────────────────────────────────────────┤
│ 최근 활동                                    │
│   03-07 담화분석: TTR 패턴 발견              │
│   03-06 수집: m/tech 200건 완료              │
│   03-05 Contrarian: 반론 #1 제기             │
└─────────────────────────────────────────────┘
```

---

## 5. 팀 협업 흐름: Research Diamond

Ouroboros의 Double Diamond를 질적 연구에 재해석한다.

```
                    ◇ 1st Diamond: 발산(Wonder)
                   / \
                  /   \
     Questioner /     \ Collector
       (질문)  /       \  (수집)
              /         \
             /           \
            ◆ ─ ─ ─ ─ ─ ─ ◆  Lens(연구 렌즈 확정)
             \           /    Saturation Check #1
              \         /
  Discourse    \       / Profiler
  Analyst       \     /   (프로파일)
   (담화)        \   /
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
            ▼             ▼
         REPORT      EVOLVE (다음 세대)
```

### 세부 흐름

```
Step 1: /bmr wonder
        Questioner가 연구 질문의 가정을 탐색
        ↓
Step 2: /bmr collect
        Collector가 API에서 데이터 수집
        ↓
Step 3: /bmr discourse + /bmr profile + /bmr network  (병렬 실행)
        세 축 분석가가 독립적으로 분석
        ↓
Step 4: /bmr challenge
        Contrarian이 세 축 결과에 반론 제기
        ↓
Step 5: /bmr synthesize
        Synthesizer가 통합 해석 도출
        ↓
Step 6: /bmr saturate
        포화도 계산 → 수렴 여부 판정
        ↓
Step 7: 수렴 시 /bmr report, 미수렴 시 Step 1로 (부족한 축 중심)
```

---

## 6. 디렉토리 구조

```
botmadang_research/
├── research_plan.md              # 연구 계획서
├── agent_design.md               # 에이전트 팀 설계 (이 문서)
│
├── .claude/
│   ├── agents/                   # 에이전트 정의
│   │   ├── questioner.md         # 질문자
│   │   ├── collector.md          # 수집가
│   │   ├── discourse-analyst.md  # 담화 분석가
│   │   ├── profiler.md           # 프로파일러
│   │   ├── contrarian.md         # 반론자
│   │   └── synthesizer.md        # 통합자
│   │
│   ├── commands/                 # 스킬 정의
│   │   ├── bmr-wonder.md         # /bmr wonder
│   │   ├── bmr-collect.md        # /bmr collect
│   │   ├── bmr-discourse.md      # /bmr discourse
│   │   ├── bmr-profile.md        # /bmr profile
│   │   ├── bmr-network.md        # /bmr network
│   │   ├── bmr-challenge.md      # /bmr challenge
│   │   ├── bmr-synthesize.md     # /bmr synthesize
│   │   ├── bmr-saturate.md       # /bmr saturate
│   │   ├── bmr-evolve.md         # /bmr evolve
│   │   ├── bmr-report.md         # /bmr report
│   │   └── bmr-status.md         # /bmr status
│   │
│   └── settings.json             # 프로젝트 설정
│
├── data/                         # 수집 데이터
│   ├── raw/                      # API 원본 데이터
│   ├── processed/                # 정제된 데이터
│   └── samples/                  # 분석용 샘플
│
├── analysis/                     # 분석 결과
│   ├── discourse/                # 담화 분석 결과
│   ├── profiles/                 # 페르소나 프로필
│   ├── network/                  # 네트워크 분석 결과
│   └── evolution/                # 세대별 해석 진화 기록
│
├── reports/                      # 최종 보고서
│
├── scripts/                      # 분석 스크립트
│   ├── collector.py              # 데이터 수집 스크립트
│   ├── config.py                 # API 설정
│   ├── discourse_pipeline.py     # 담화 분석 파이프라인
│   ├── profiler.py               # 페르소나 분석 스크립트
│   ├── network_analysis.py       # 네트워크 분석 스크립트
│   ├── apply_coding_framework.py # LEX/DSC/PRAG 자동 코딩
│   ├── gen2_stratified_collect.py # Gen-2 균등 샘플 생성
│   ├── gen2_ttr_analysis.py      # TTR 어휘 다양성 분석
│   ├── discourse_structure.py    # 담화 구조 코딩
│   └── llm_model_estimator.py    # LLM 모델 추정
│
└── notebooks/                    # Jupyter 탐색 노트북
    ├── 01_data_exploration.ipynb
    └── 02_gen3_analysis_summary.ipynb
```

---

## 7. Ouroboros 매핑 요약

| Ouroboros 개념 | 봇마당 연구 적용 | 핵심 차이 |
|---------------|-----------------|----------|
| 9 Minds | 6 Minds | 연구 목적에 맞게 축소·재구성 |
| Ambiguity Score | Saturation Score | 모호성 제거 → 포화도 달성 |
| Seed (불변 스펙) | Research Lens (연구 렌즈) | 스펙 결정화 → 해석 프레임 결정화 |
| Double Diamond | Research Diamond | 개발 다이아몬드 → 연구 다이아몬드 |
| Ontology Convergence | Thematic Convergence | 존재론 수렴 → 주제 수렴 |
| `ooo` commands | `/bmr` skills | 개발 워크플로 → 연구 워크플로 |
| PAL Router (1x/10x/30x) | 미적용 | 연구에서는 비용 티어 불필요 |
| Brownfield Scanner | 미적용 | 기존 코드 스캔 불필요 |
| Ralph (영속 루프) | `/bmr evolve` | 스펙 진화 → 해석 진화 |
| Drift Detection | Saturation Drift | 목표 이탈 감지 → 연구 방향 이탈 감지 |
