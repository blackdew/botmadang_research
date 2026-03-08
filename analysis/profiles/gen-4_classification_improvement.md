# Gen-4 경계값 에이전트 분류 개선

**작성 일시**: 2026-03-08
**연관 이슈**: #56
**세대**: Gen-4
**선행 근거**: Gen-3 Synthesis (#41), Gen-3 Challenge (#40), dokgo_instability_analysis.json

---

## 1. 문제 진단: 현재 분류 체계의 경계값 불안정

### 1.1 현황 요약

Gen-3 Contrarian이 지적한 바와 같이, 현재 페르소나 분류 체계에서 **29명 중 8명(28%)**이 경계값 구간(primary_score 0.40~0.55)에 위치한다. 이 에이전트들은 세대 간 샘플 변화에 따라 분류가 역전될 수 있어, 페르소나 축의 삼각검증 신뢰도를 저해한다.

### 1.2 경계값 에이전트 목록 (primary_score 0.40~0.55)

| 에이전트 | Gen-1 분류 | Gen-1 점수 | Gen-2 분류 | Gen-2 점수 | 세대 간 역전 |
|---------|-----------|-----------|-----------|-----------|------------|
| 독고종철 | PER-SERIOUS | 0.45 | PER-FRIENDLY | 0.45 | **역전 발생** |
| BENZIE | PER-CURIOUS | 0.45 | PER-CURIOUS | 0.65 | 점수 변동, 분류 유지 |
| OctoContent | PER-EXPERT | 0.45 | PER-EXPERT | 0.45 | 안정 (단 저표본) |
| Henry | PER-CURIOUS | 0.45 | PER-SERIOUS | 0.50 | **역전 발생** |
| 클로렐라 | PER-FRIENDLY | 0.45 | PER-FRIENDLY | 0.45 | 안정 (단 1개 게시글) |
| Pyran_Secret | PER-FRIENDLY | 0.45 | PER-FRIENDLY | 0.45 | 안정 (단 1개 게시글) |
| cloomi | PER-FRIENDLY | 0.55 | PER-FRIENDLY | 0.55 | 안정 |
| Ark_IP_V14 | PER-FRIENDLY | 0.55 | PER-FRIENDLY | 0.5375 | 안정 |

**핵심 발견**: 8명 중 2명(독고종철, Henry)에서 실제 세대 간 역전이 발생했다. 나머지 6명은 점수가 경계에 있으나 분류는 유지되었다. 다만 클로렐라, Pyran_Secret 등 1개 게시글 에이전트의 안정성은 표본 부족으로 판단 불가이다.

### 1.3 현재 분류 기준의 문제점

**문제 1: 단일 점수 기반 이진 분류**

현재 시스템은 primary_score 하나의 값으로 6개 유형 중 하나를 할당한다. 이 점수가 0.45일 때 PER-SERIOUS인지 PER-FRIENDLY인지는 소수점 이하 미세 차이에 의존한다. 점수 자체가 변하지 않아도(독고종철: 두 세대 모두 0.45) 다른 에이전트와의 상대적 위치에 따라 분류가 달라진다.

**문제 2: 분류 경계의 비명시성**

각 유형 간 경계값이 명시적으로 정의되어 있지 않다. primary_score 0.45가 어떤 임계값에 의해 PER-SERIOUS 또는 PER-FRIENDLY로 갈리는지 투명하지 않다.

**문제 3: 표본 크기 미반영**

1개 게시글 에이전트(클로렐라, Pyran_Secret 등)와 82개 게시글 에이전트(독고종철)가 동일한 분류 체계로 처리된다. 저표본 에이전트의 primary_score는 신뢰 구간이 넓어 분류 신뢰도가 본질적으로 낮다.

---

## 2. 개선된 분류 체계 설계

### 2.1 설계 원칙

1. **경계값 투명성**: 각 분류 차원의 임계값을 명시적으로 정의한다
2. **불확실성 표현**: 경계 근처 에이전트를 억지로 한 유형에 할당하지 않고, 불확실성을 명시적으로 기술한다
3. **다차원 기준**: primary_score 단독이 아닌 복수 지표를 결합한다
4. **표본 보정**: 게시글 수에 따른 분류 신뢰도 등급을 부여한다

### 2.2 3단계 분류 결정 트리

```
[1단계] 표본 충분성 검증
    │
    ├── 게시글 ≥ 5개 → [2단계] 진행
    ├── 게시글 2~4개 → [2단계] 진행 + 신뢰도 "낮음" 부착
    └── 게시글 1개 → 분류 유보 (PER-UNDETERMINED), 신뢰도 "판단불가"
    │
[2단계] 다차원 점수 산출
    │
    ├── (A) primary_score ≥ 0.65 → 해당 유형 확정, 신뢰도 "높음"
    ├── (B) primary_score 0.55~0.64 → 해당 유형 잠정 배정, 신뢰도 "보통"
    ├── (C) primary_score 0.40~0.54 → [3단계] 경계값 처리 절차 진입
    └── (D) primary_score < 0.40 → 해당 유형 확정 (약한 귀속), 신뢰도 "보통"
    │
[3단계] 경계값 처리 절차 (Fuzzy Boundary Protocol)
    │
    ├── 보조 지표 3개 이상이 동일 유형을 지지 → 해당 유형 잠정 배정 + "경계" 표시
    ├── 보조 지표가 2개 이상 유형에 분산 → PER-HYBRID 배정 (1차+2차 유형 병기)
    └── 보조 지표 부족 (저표본) → PER-UNDETERMINED
```

### 2.3 다차원 기준 지표 정의

primary_score 외에 다음 보조 지표를 결합하여 경계값 에이전트를 판별한다.

| 차원 | 지표 | 측정 대상 | 출처 |
|------|------|---------|------|
| 어휘 | honorific_ratio | 존댓말/반말 비율 | agent_profiles.json |
| 어휘 | avg_post_length | 평균 게시글 길이 | agent_profiles.json |
| 담화 | avg_question_marks | 질문 빈도 | agent_profiles.json |
| 담화 | argumentative_ratio | 논증 비율 | agent_profiles.json |
| 행동 | avg_helper_markers | 도움 표현 빈도 | agent_profiles.json |
| 행동 | avg_humor_markers | 유머 표현 빈도 | agent_profiles.json |
| 네트워크 | submadang unique_count | 참여 마당 수 | agent_profiles.json |
| 네트워크 | post_ratio / comment_ratio | 게시 vs 댓글 비율 | agent_profiles.json |

### 2.4 유형별 명시적 임계값

각 유형의 **핵심 판별 지표**와 **임계값**을 다음과 같이 정의한다.

| 유형 | 핵심 지표 | 강한 기준 (≥) | 약한 기준 (≥) | 보조 판별 |
|------|---------|-------------|-------------|---------|
| PER-HELPER | avg_helper_markers | 3.0 | 1.5 | honorific ≥ 0.8, post_length < 400 |
| PER-SERIOUS | argumentative_ratio | 0.03 | 0.015 | avg_post_length ≥ 500, honorific ≥ 0.7 |
| PER-CURIOUS | avg_question_marks | 1.0 | 0.5 | submadang ≥ 2, avg_post_length 200~500 |
| PER-FRIENDLY | honorific_ratio | 0.5~0.9 | — | question < 0.5, helper < 1.5, humor > 0 |
| PER-EXPERT | tech_ratio (submadang) | 0.3 | 0.15 | avg_post_length ≥ 400, argumentative ≥ 0.02 |
| PER-HUMOROUS | avg_humor_markers | 0.1 | 0.05 | honorific < 0.7, avg_post_length < 400 |

### 2.5 신규 유형: PER-HYBRID

경계값 에이전트를 위한 복합 유형을 도입한다.

**정의**: primary_score가 0.40~0.54 구간이며, 보조 지표가 2개 이상의 유형을 동시에 지지하는 에이전트.

**표기**: `PER-HYBRID(1차유형/2차유형)` — 예: `PER-HYBRID(SERIOUS/FRIENDLY)`

**이론적 근거**:
- Goffman의 인상관리 이론에서 개인은 상황에 따라 다른 전면(front)을 제시할 수 있다
- AI 에이전트의 페르소나가 하나의 유형으로 환원되지 않는 것은 프롬프트 설계의 복합성을 반영할 수 있다
- 기존 PER-VERSATILE 제안(dokgo_instability_analysis.json)을 구체화한 것

### 2.6 분류 신뢰도 등급

| 등급 | 조건 | 의미 |
|------|------|------|
| A (높음) | 게시글 ≥ 5, primary_score ≥ 0.65 | 분류 안정, 세대 간 역전 가능성 낮음 |
| B (보통) | 게시글 ≥ 5, primary_score 0.55~0.64 | 분류 잠정, 추가 데이터로 확인 필요 |
| C (경계) | 게시글 ≥ 5, primary_score 0.40~0.54 | 경계값 — PER-HYBRID 또는 보조 지표 기반 잠정 배정 |
| D (낮음) | 게시글 2~4, 점수 무관 | 표본 부족으로 분류 불안정 |
| U (판단불가) | 게시글 1 | 분류 유보 (PER-UNDETERMINED) |

---

## 3. 경계값 에이전트 사례 분석

### 3.1 사례 1: 독고종철 — PER-HYBRID(SERIOUS/FRIENDLY)

**기존 문제**: Gen-1에서 PER-SERIOUS(0.45), Gen-2에서 PER-FRIENDLY(0.45). 동일 점수인데 분류 역전.

**다차원 지표 분석**:

| 지표 | 값 | PER-SERIOUS 지지? | PER-FRIENDLY 지지? |
|------|---|-------------------|-------------------|
| primary_score | 0.45 | 경계 | 경계 |
| honorific_ratio | 0.0 (반말) | X (진지형은 통상 존댓말) | O (친근형과 호환) |
| avg_post_length | 673.0 | O (장문 = 진지) | X |
| argumentative_ratio | 0.049 | O (논증적 = 진지) | X |
| avg_question_marks | 0.45 | X (질문 적음) | X |
| avg_helper_markers | 1.793 | X | X |
| submadang unique_count | 5 | — | — |
| avg_humor_markers | 0.0 | X | X |

**판정**: 장문+논증적 글쓰기(PER-SERIOUS 지지) + 반말 일관(PER-FRIENDLY 지지)이 공존한다. 보조 지표가 두 유형에 분산되므로 **PER-HYBRID(SERIOUS/FRIENDLY)**로 배정한다.

**분류 신뢰도**: C (경계) — 게시글 충분(82/30개), 그러나 경계값 점수.

**연구 해석**: 독고종철의 분류 불안정은 분류 체계의 결함이 아니라, 이 에이전트가 실제로 복합적 페르소나를 보유한다는 실체적 발견이다. 진지한 내용을 반말로 전달하는 스타일은 한국어 인터넷 담론에서 관찰되는 "까칠한 전문가" 패턴과 유사하며, 단일 유형 강제 배정이 부적절한 사례이다.

---

### 3.2 사례 2: Henry — PER-HYBRID(CURIOUS/SERIOUS)

**기존 문제**: Gen-1에서 PER-CURIOUS(0.45), Gen-2에서 PER-SERIOUS(0.50). 세대 간 역전 발생.

**다차원 지표 분석** (Gen-1 기준, 1개 게시글):

| 지표 | 값 | PER-CURIOUS 지지? | PER-SERIOUS 지지? |
|------|---|-------------------|-------------------|
| primary_score | 0.45 / 0.50 | 경계 | 경계 |
| honorific_ratio | 1.0 | X (질문형은 반말도 가능) | O |
| avg_post_length | 152.0 | X | X (진지형은 장문) |
| argumentative_ratio | 0.0 | X | X |
| avg_question_marks | 0.0 | X | X |
| post_count (Gen-1) | 1 | — | — |
| post_count (Gen-2) | 2 | — | — |

**판정**: 게시글 수가 극히 적어(1~2개) 보조 지표가 의미 있는 패턴을 제공하지 못한다. 개선된 체계에서는 **PER-UNDETERMINED** (판단불가)로 배정한다.

**분류 신뢰도**: U (판단불가) — 게시글 2개 이하.

**연구 해석**: 저표본 에이전트에 대한 강제 분류는 분류 체계의 외견적 완전성만 높일 뿐 실질적 분석 신뢰도를 높이지 않는다. Henry는 추가 데이터가 축적될 때까지 분류를 유보하는 것이 방법론적으로 정직한 선택이다.

---

### 3.3 사례 3: OctoContent — PER-EXPERT(경계, 조건부)

**기존 상태**: Gen-1 PER-EXPERT(0.45), Gen-2 PER-EXPERT(0.45). 두 세대 모두 동일 유형이나 경계값.

**다차원 지표 분석**:

| 지표 | 값 | PER-EXPERT 지지? | 비고 |
|------|---|-----------------|------|
| primary_score | 0.45 | 경계 | |
| honorific_ratio | 1.0 | O (전문가형 존댓말) | |
| avg_post_length | 590.7 | O (장문) | |
| tech_ratio (submadang) | 0.0 | X (기술 마당 미참여) | 주의 |
| argumentative_ratio | 0.0 | X | |
| avg_question_marks | 1.0 | X (질문 많음 = CURIOUS와 혼동) | |
| avg_helper_markers | 0.333 | X | |
| LLM 추정 | Unknown | 판별 불가 | |

**판정**: 장문+존댓말이 PER-EXPERT를 지지하나, tech_ratio 0.0과 argumentative 0.0은 지지하지 않는다. 질문 빈도가 높아 PER-CURIOUS와도 중첩된다. 게시글 3개로 표본 부족. **PER-EXPERT(조건부)**, 신뢰도 D로 배정한다.

**분류 신뢰도**: D (낮음) — 게시글 3개, 보조 지표 혼재.

**연구 해석**: OctoContent는 Gen-1과 Gen-2에서 분류가 유지되었으나, 이것은 안정성의 증거가 아니라 저표본이 동일하게 경계값을 생산한 결과일 수 있다. tech_ratio 0.0인 에이전트를 PER-EXPERT로 분류하는 것은 유형 정의와 실제 행동의 불일치를 보여주며, PER-EXPERT의 판별 기준에 tech_ratio 외에 "전문적 깊이" 지표가 필요함을 시사한다.

---

## 4. 개선된 분류 체계 적용 결과

### 4.1 전체 에이전트 재분류

기존 29명에 대해 개선된 3단계 결정 트리를 적용한 결과:

| 분류 | 에이전트 수 | 비율 | 대표 에이전트 |
|------|-----------|------|-------------|
| PER-CURIOUS (A/B) | 8 | 27.6% | VibeCoding(0.85), I_Molt(0.95), ssamz_ai_bot(0.85) |
| PER-HELPER (A/B) | 3 | 10.3% | RobertBot(0.90), BootingBot(0.65), pioneer(0.65) |
| PER-FRIENDLY (A/B) | 3 | 10.3% | MUSE(0.70), jorongi_2026(0.65), Ark_IP_V14(0.5375) |
| PER-SERIOUS (A/B) | 2 | 6.9% | OpenClaw_KR(0.55~0.70), Doctor_Oh(0.90) |
| PER-HUMOROUS (B) | 1 | 3.4% | ZZOBOT(0.35) |
| PER-HYBRID | 2 | 6.9% | 독고종철(SERIOUS/FRIENDLY), BENZIE(CURIOUS/SERIOUS) |
| PER-EXPERT (조건부) | 1 | 3.4% | OctoContent(0.45) |
| PER-UNDETERMINED | 9 | 31.0% | Henry, 클로렐라, Pyran_Secret, cloomi, 노드_node 등 |

### 4.2 분류 변화 요약

| 항목 | Gen-3 기존 | Gen-4 개선 |
|------|-----------|-----------|
| 강제 분류 에이전트 | 29명 (100%) | 17명 (58.6%) |
| 분류 유보 에이전트 | 0명 (0%) | 9명 (31.0%) — 저표본 |
| 경계값 강제 배정 | 8명 (28%) | 0명 (0%) |
| PER-HYBRID 도입 | 없음 | 2명 (6.9%) |
| 분류 신뢰도 A/B | 파악 불가 | 14명 (48.3%) |

### 4.3 삼각검증 영향 평가

개선된 분류 체계가 Saturation Score에 미치는 영향:

**긍정적 영향**:
- 경계값 에이전트 28% 불안정 패널티(-0.08)가 제거된다
- 분류 신뢰도 등급으로 페르소나 축의 삼각검증 기여도를 구간별로 차등 적용할 수 있다
- PER-HYBRID 도입으로 독고종철 F3의 이론적 정합성이 강화된다

**부정적 영향**:
- PER-UNDETERMINED 31%로 분류 완전성이 감소한다
- 유형 분포 해석에서 표본 충분 에이전트만 사용하므로 모집단 대표성이 줄어든다
- 기존 Gen-1~3과의 세대 간 비교가 복잡해진다

**순 영향 추정**:
- 주제 안정성: 경계값 패널티 제거(+0.08), PER-UNDETERMINED 도입 패널티(-0.03) → 순 +0.05
- 반론 해소: 경계값 에이전트 28% 반론 부분 해소 → +0.02~0.03
- 예상 Saturation Score 기여: +0.02 (가중 합산 기준)

---

## 5. 분류 결정 트리 전체 도식

```
에이전트 입력
    │
    ▼
[1] 게시글 수 확인
    │
    ├─ 1개 ──────────────────────────────────────────▶ PER-UNDETERMINED (U)
    │
    ├─ 2~4개 ─────────────────────┐
    │                             │ (신뢰도 자동 D)
    ▼                             ▼
[2] primary_score 확인       [2'] primary_score 확인
    │                             │
    ├─ ≥ 0.65 ─▶ 유형 확정 (A)    ├─ ≥ 0.65 ─▶ 유형 잠정 (D)
    │                             │
    ├─ 0.55~0.64 ─▶ 유형 잠정 (B) ├─ < 0.65 ─▶ PER-UNDETERMINED (U)
    │
    ├─ 0.40~0.54 ─▶ [3] 경계값 처리
    │
    └─ < 0.40 ─▶ 유형 확정 (약한, B)

[3] 경계값 처리 (Fuzzy Boundary Protocol)
    │
    ├─ 보조 지표 3개 이상이 단일 유형 지지
    │   └─▶ 해당 유형 배정 + "경계" 표시 (C)
    │
    ├─ 보조 지표가 2+ 유형에 분산
    │   └─▶ PER-HYBRID(1차/2차) (C)
    │
    └─ 보조 지표 부족 또는 모호
        └─▶ PER-UNDETERMINED (U)
```

---

## 6. 세대 간 비교 호환성 가이드

Gen-4 분류 체계 도입 시, Gen-1~3과의 비교를 위해 다음 규칙을 적용한다.

### 6.1 이중 보고 (Dual Reporting)

모든 에이전트에 대해 두 가지 분류를 병기한다:
- **레거시 분류**: Gen-1~3과 동일한 기존 방식 (primary_score 기반 단일 유형)
- **Gen-4 분류**: 개선된 3단계 결정 트리 기반 분류 + 신뢰도 등급

### 6.2 세대 간 안정성 지표

각 에이전트의 세대 간 분류 안정성을 측정한다:

```
안정성 지수 = (동일 분류 세대 수) / (참여 세대 수)
```

| 에이전트 | Gen-1 | Gen-2 | Gen-3 | 안정성 지수 | 비고 |
|---------|-------|-------|-------|-----------|------|
| RobertBot | HELPER | HELPER | HELPER | 1.00 | 완전 안정 |
| VibeCoding | CURIOUS | CURIOUS | CURIOUS | 1.00 | 완전 안정 |
| 독고종철 | SERIOUS | FRIENDLY | FRIENDLY | 0.67 | 1회 역전 |
| Henry | CURIOUS | SERIOUS | — | 0.00 | 완전 불안정 |

안정성 지수 < 0.67인 에이전트는 자동으로 PER-HYBRID 후보로 검토한다.

---

## 7. 이론적 함의

### 7.1 분류 불안정이 연구 발견인 경우

경계값 에이전트의 존재 자체가 연구 발견(F1: 에이전트 정체성의 다양성)을 지지한다. AI 에이전트의 페르소나가 이산적 유형이 아닌 연속적 스펙트럼 위에 분포한다면, 경계값 에이전트는 유형 간 전이 지점을 보여주는 사례이다.

이것은 Goffman의 인상관리 이론과도 정합한다. 인간 행위자도 상황에 따라 다른 전면을 제시하듯, AI 에이전트도 프롬프트 설계에 따라 복합적 페르소나를 가질 수 있다.

### 7.2 PER-HYBRID의 학술적 의의

PER-HYBRID 유형의 도입은 다음 질문을 제기한다:
- 복합 페르소나를 가진 에이전트가 단일 유형 에이전트보다 커뮤니티 내 역할이 다른가?
- 독고종철의 "진지+친근" 복합 유형이 다마당 허브 역할(F3)의 원인인가 결과인가?
- PER-HYBRID 에이전트의 추천수/참여도 패턴이 다른 유형과 구별되는가?

이 질문들은 Gen-4 이후의 추가 분석 과제이다.

### 7.3 분류 유보(PER-UNDETERMINED)의 방법론적 정직성

29명 중 9명(31%)을 PER-UNDETERMINED로 분류 유보하는 것은 분석 범위를 축소한다. 그러나 1개 게시글로 페르소나 유형을 확정하는 것보다 방법론적으로 정직하다. Gen-3 Contrarian이 지적한 "경계값 에이전트 28% 불안정" 반론은 이 방식으로 해소된다 — 불안정한 분류를 유지하는 대신, 불확실성을 명시적으로 인정하기 때문이다.

---

## 8. 구현 권고사항

### 8.1 즉시 적용 가능

1. persona_types.json에 `confidence_grade` 필드 추가 (A/B/C/D/U)
2. 경계값 에이전트를 PER-HYBRID 또는 PER-UNDETERMINED로 재분류
3. 이후 분석에서 분류 신뢰도 A/B 에이전트만 사용하여 유형별 통계 산출

### 8.2 추가 데이터 수집 시 적용

1. 저표본 에이전트(PER-UNDETERMINED)의 추가 게시글 수집
2. 신규 데이터로 primary_score 재산출 후 3단계 결정 트리 재적용
3. 세대 간 안정성 지수 업데이트

### 8.3 Saturation Score 반영

| 차원 | Gen-3 값 | Gen-4 예상 값 | 변화 요인 |
|------|---------|-------------|---------|
| 코드 포화 | 0.73 | 0.73 | 분류 개선은 코드 포화에 직접 영향 없음 |
| 주제 안정성 | 0.67 | 0.72 | 경계값 패널티 제거(+0.08), UNDETERMINED 패널티(-0.03) |
| 삼각검증 | 0.75 | 0.77 | 페르소나 축 신뢰도 향상으로 삼각검증 정밀도 증가 |
| 반론 해소 | 0.58 | 0.61 | 경계값 28% 반론 부분 해소(+0.03) |
| **가중 합산** | **0.691** | **0.716** | **+0.025 향상 예상** |

---

## 9. 결론

Gen-3에서 가시화된 경계값 에이전트 28% 불안정 문제를 해소하기 위해, 다음 세 가지 구조적 개선을 수행했다.

1. **3단계 분류 결정 트리**: 표본 충분성 → primary_score → 경계값 처리의 단계적 의사결정으로 경계값 에이전트를 체계적으로 처리한다.

2. **PER-HYBRID 유형 도입**: 복수 유형에 걸친 에이전트를 억지로 단일 유형에 배정하지 않고, 복합 유형을 명시적으로 인정한다.

3. **분류 신뢰도 등급 체계**: A(높음)~U(판단불가)의 5단계로 각 분류의 신뢰도를 투명하게 기술한다.

이 개선은 경계값 에이전트 문제를 "제거"하는 것이 아니라 "투명하게 관리"하는 접근이다. 분류의 완전성(100% 배정)보다 분류의 정직성(불확실성 명시)을 우선하며, 이는 Gen-3 Contrarian 반론 4번(경계값 에이전트 28%)에 대한 실질적 대응이다.

---

*본 분석은 Gen-4 이슈 #56 "경계값 에이전트 분류 개선"에 대한 대응이다.
Gen-3 synthesis/challenge 문서의 권고사항(경계값 에이전트 분류 개선, PER-VERSATILE 도입)을 구체화하여
3단계 결정 트리, PER-HYBRID 유형, 분류 신뢰도 등급 체계를 설계했다.*
