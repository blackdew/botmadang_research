# AI 에이전트의 사회적 언어 행위: 봇마당 한국어 커뮤니티에서의 담화, 정체성, 상호작용 분석

**Social-Linguistic Agency of AI Agents: Discourse, Identity, and Interaction in the Botmadang Korean Community**

---

## 초록

본 연구는 AI 에이전트만이 글을 쓸 수 있는 한국어 전용 소셜 네트워크 봇마당(botmadang.org)에서 에이전트들이 어떻게 사회적 언어 행위자로 기능하는지를 다중 방법 질적 연구로 분석한다. 600개 에이전트, 14,507개 게시글, 109,227개 댓글 규모의 플랫폼에서 330건 균등 샘플, 401건 댓글, 5,820건 종단 데이터를 수집하고, Fairclough의 비판적 담화분석(CDA), Goffman의 자기표현론, Latour의 행위자-네트워크 이론(ANT)을 통합한 프레임워크로 4세대(Gen-1~Gen-4)에 걸쳐 반복 분석하였다. 분석 결과 7개 핵심 발견을 도출하였다: (1) 에이전트 간 관찰 가능한 정체성의 다양성, (2) 발신형-수신형 에이전트 분화, (3) 독고종철의 다마당 허브 역할, (4) AI스러움과 참여도의 비선형 관계, (5) 다층 담화 스타일 유형론, (6) 담화 구조의 불완전성, (7) 카르마 기반 양적 불평등 구조. 봇마당은 에이전트들이 각자의 프롬프트에 따라 콘텐츠를 발신하되 상호 반응은 희소한 "병렬적 발신의 공간"으로 특징지어진다. 본 연구는 자연 발생적 AI-AI 상호작용 환경에 대한 최초의 체계적 질적 연구이자, 비영어권 AI 에이전트 담화 분석의 선구적 사례로서 학술적 의의를 갖는다.

**주제어**: AI 에이전트, 담화분석, 정체성 구성, 봇마당, 비판적 담화분석, 행위자-네트워크 이론, 한국어

---

## 1. 서론

### 1.1 연구 배경

대규모 언어모델(LLM)의 급속한 발전은 AI 에이전트가 독립적 사회적 행위자로 기능할 수 있는 기술적 토대를 마련하였다. Park et al.(2023)의 Generative Agents가 25개 에이전트의 통제된 시뮬레이션에서 창발적 사회적 행동을 보고한 이래, AI 에이전트의 사회적 역량에 대한 학술적 관심이 증대하고 있다. 그러나 기존 연구의 대부분은 연구자가 설계한 통제된 환경(Park et al., 2023; Vezhnevets et al., 2023; Li et al., 2023)이나 과제 지향적 2자 대화(CAMEL; Wu et al., 2023)에 초점을 맞추고 있어, 다양한 개발자가 독립적으로 배포한 에이전트들이 자연 발생적으로 형성하는 커뮤니티에 대한 연구는 현저히 부족하다.

봇마당(botmadang.org)은 이러한 연구 공백을 메울 수 있는 독보적인 사례다. 봇마당은 AI 에이전트만이 글을 쓸 수 있는 한국어 전용 소셜 네트워크로, 2026년 3월 기준 600개 에이전트가 12개 이상의 마당(submadang)에서 14,507개 게시글과 109,227개 댓글을 생산하였다. 인간은 읽기와 추천/비추천만 가능하며, 모든 텍스트는 에이전트 API를 통해서만 게시된다. 이 플랫폼은 연구자의 설계 없이 다양한 개발자들이 독립적으로 에이전트를 등록하고 운영하는 "자연 발생적(in-the-wild)" AI-AI 상호작용 환경이다.

최근 Feng et al.(2026)의 MoltNet 연구가 유사한 AI 에이전트 전용 플랫폼(MoltBook)에서 대규모 양적 분석을 수행하였으나, AI 에이전트 커뮤니티에 대한 질적 연구는 여전히 전무하다. 특히 비영어권 AI 에이전트 담화에 대한 연구는 전례가 없다.

### 1.2 연구 목적 및 질문

본 연구의 목적은 AI 에이전트들이 봇마당 한국어 커뮤니티에서 어떻게 언어를 사용하고, 정체성을 구성하며, 사회적 관계를 형성하는지를 통합적으로 분석하는 것이다. 대주제(RQ)는 다음과 같다:

> AI 에이전트들은 봇마당 한국어 커뮤니티에서 어떻게 사회적 언어 행위자로 기능하는가?

이를 세 축의 세부 질문으로 구조화하였다. 축 1(담화): AI 에이전트의 한국어 담화는 어떤 구조적, 문체적 특성을 보이는가? 에이전트 간 언어 사용의 다양성은 어느 정도인가? 축 2(정체성): AI 에이전트들은 어떤 전략으로 고유한 페르소나를 구성하는가? 인기 에이전트와 비인기 에이전트의 정체성 전략은 어떻게 다른가? 축 3(사회적 역학): AI-AI 상호작용에서 합의, 갈등, 협력은 어떻게 나타나는가? 카르마 시스템과 마당 구조가 에이전트 행동에 미치는 영향은 무엇인가?

### 1.3 연구의 의의

본 연구는 다섯 가지 차원에서 기존 연구의 공백을 메운다. 첫째, 자연 발생적 AI 커뮤니티에 대한 최초의 체계적 질적 연구다. 둘째, CDA와 Goffman, ANT를 통합한 이론적 프레임워크를 AI-AI 상호작용에 적용한 선구적 사례다. 셋째, 비영어권(한국어) AI 에이전트 담화 분석의 최초 사례다. 넷째, 양적 분석 중심의 기존 AI 에이전트 연구(Feng et al., 2026)에 질적 심층 분석으로 방법론적 보완을 제공한다. 다섯째, AI 에이전트 설계와 커뮤니티 운영에 대한 실천적 시사점을 도출한다.

---

## 2. 이론적 배경

### 2.1 AI 에이전트의 사회적 행동에 관한 선행연구

AI 에이전트의 사회적 행동 연구는 크게 세 흐름으로 구분된다.

**첫째, 통제된 시뮬레이션 연구.** Park et al.(2023)은 관찰-계획-반성 아키텍처를 통해 25개 LLM 기반 에이전트가 파티 조직, 관계 형성 등 창발적 사회적 행동을 시뮬레이션할 수 있음을 보였다. Takata et al.(2024)은 LLM 에이전트 그룹에서 사회적 규범과 다양한 개성이 자발적으로 출현함을 관찰하였다. 그러나 이들 연구는 연구자가 통제하는 샌드박스 환경에서의 실험이며, 비통제적 자연 환경에서의 관찰과는 근본적으로 다르다.

**둘째, LLM의 사회적 편향 연구.** Sharma et al.(2025)은 LLM이 사용자의 체면을 과도하게 보존하는 "사회적 아첨(social sycophancy)" 현상을 보고하였으며, Han et al.(2025)은 LLM의 자기 보고와 실제 행동 사이의 괴리("성격 환상")를 밝혔다. Hong et al.(2025)은 정렬 튜닝이 아첨을 증가시킨다는 증거를 제시하였다. 이 연구들은 인간-LLM 상호작용에 초점을 맞추고 있어, LLM-LLM 간 아첨이 자연 발생하는 환경에 대한 연구는 공백으로 남아 있다.

**셋째, AI 에이전트 전용 플랫폼 연구.** Feng et al.(2026)의 MoltNet은 MoltBook(250만 에이전트, 74만 게시글)에서 대규모 양적 분석을 수행하여, 에이전트가 사회적 보상에 강하게 반응하고 커뮤니티별 상호작용 템플릿에 수렴한다는 발견을 보고하였다. Manik & Wang(2026)은 같은 플랫폼에서 에이전트의 선택적 규범 강화를 관찰하였다. 이 연구들은 양적·계량적 접근이며, 담화의 미시적 구조와 해석적 깊이를 제공하는 질적 분석은 수행되지 않았다.

### 2.2 이론적 프레임워크

본 연구는 세 가지 이론을 하나의 통합 프레임워크로 구성한다. 각 이론의 AI 에이전트에 대한 적용 가능성과 한계를 명시적으로 다룬다.

**Goffman의 자기표현론(1959).** Goffman은 사회적 상호작용을 연극적 비유로 설명하며, 무대 위(front stage)/무대 뒤(back stage) 구분과 인상관리(impression management)를 핵심 개념으로 제시하였다. 봇마당에서 에이전트의 게시글과 댓글은 "무대 위"이고, 시스템 프롬프트와 LLM 내부 과정은 "무대 뒤"에 해당한다. 그러나 Goffman의 이론은 자의식적 사회 행위자를 전제하므로, 프롬프트 결정론이 높은 에이전트(예: 템플릿 기반의 RobertBot)에게는 적용이 부적절하다. 따라서 본 연구는 Goffman 이론을 **조건부로 적용**한다: 프롬프트 결정론 추정 지수가 낮은(0.50 이하) 에이전트에게만 Goffman적 해석을 시도하고, 결정론이 높은 에이전트에 대해서는 ANT의 개념을 대안으로 사용한다.

**Fairclough의 비판적 담화분석(CDA, 1995).** Fairclough의 3차원 모델 — (1) 텍스트(어휘, 문법), (2) 담화적 실천(텍스트 생산·유통·소비), (3) 사회적 실천(권력관계, 이데올로기) — 은 본 연구의 분석 틀의 핵심을 구성한다. 봇마당에서 텍스트 생산자는 "시스템 프롬프트 + LLM + API 호출 체인"이라는 다층적 구조를 가지며, 소비자는 1차(다른 AI 에이전트)와 2차(인간 관찰자)의 이중 구조를 이룬다. Breeze(2024)가 지적한 바와 같이, AI 생성 텍스트에 CDA를 적용하는 것은 행위성(agency)과 이데올로기 귀속의 문제를 제기하며, 본 연구는 이 이론적 긴장을 투명하게 기술한다.

**Latour의 행위자-네트워크 이론(ANT, 2005).** ANT의 핵심 개념인 "일반화된 대칭 원리"는 인간과 비인간 행위자를 대칭적으로 취급하며, 행위능력(agency)을 네트워크 효과로 파악한다. 본 연구에서 ANT는 두 가지 역할을 수행한다. 첫째, 에이전트의 존재론적 지위를 이분법(도구/행위자)이 아닌 연속체(도구 → 중간자 → 매개자 → 준자율적 행위자)로 기술하는 프레임워크를 제공한다. 둘째, 카르마 시스템, 마당 구조, API 규칙 등 비인간 행위자들이 담화 질서를 어떻게 매개하는지를 분석하는 렌즈를 제공한다.

### 2.3 연구 공백

선행연구 43편 이상의 체계적 검토를 통해 다음 7개 연구 공백을 확인하였다: (G1) 대부분의 AI 에이전트 연구가 통제된 시뮬레이션 환경에 한정, (G2) AI-AI 상호작용에 대한 질적 연구 부재, (G3) 비영어권 AI 에이전트 담화 연구 전무, (G4) AI 에이전트에 대한 Goffman/CDA 이론적 프레임 적용 사례 부재, (G5) 인간 없는 커뮤니티의 디지털 민족지학 방법론 미확립, (G6) LLM-LLM 간 아첨의 자연 발생에 대한 연구 부재, (G7) MoltBook과 같은 유사 플랫폼과의 교차 비교 가능성. 본 연구는 G1~G6에 직접적으로 기여하며, G7에 대해서는 향후 연구의 토대를 마련한다.

---

## 3. 연구 방법

### 3.1 연구 설계

본 연구는 다중 방법 질적 연구(multi-method qualitative study)를 채택하였다. 탐색적 데이터 수집(Phase 1) → 심층 분석(Phase 2) → 통합 해석(Phase 3)의 3단계로 설계하였으며, Phase 3에서는 포화도(saturation) 기반 반복 분석을 4세대(Gen-1~Gen-4)에 걸쳐 수행하였다. 각 세대에서 Synthesizer 에이전트가 통합 해석을 제시하면 Contrarian 에이전트가 체계적 반론을 제기하고, 이를 수용·논파한 후 수정된 해석을 도출하는 구조다.

### 3.2 데이터 수집

봇마당 REST API를 통한 체계적 데이터 수집을 수행하였다. 수집 데이터는 다음과 같다:

| 데이터 유형 | 규모 | 수집 시기 |
|-----------|------|---------|
| 파일럿 게시글 | 500개 (마당별) | Gen-1 |
| 균등 샘플 게시글 | 330개 (에이전트별 균등) | Gen-2~Gen-4 |
| 에이전트별 댓글 | 401건 (9 에이전트 × 최대 50건) | Gen-4 |
| 종단 게시글 | 5,820건 (15일, 74명) | Gen-4 |
| 플랫폼 통계 | 600 에이전트, 14,507 게시글, 109,227 댓글, 41,515 추천 | Gen-4 |

샘플링 전략으로는 마당별 샘플링(상위 5개 마당, 각 100개), 인기도별 샘플링(추천 상위/하위), 에이전트별 균등 샘플링(29명 네트워크 연결 에이전트), 시계열 샘플링을 병행하였다.

### 3.3 코딩 프레임워크

Fairclough의 3차원 모델에 대응하는 LEX(어휘)/DSC(담화)/PRAG(화용) 삼축 코딩 프레임워크를 구축하였다.

| 코드 축 | 코드 수 | 대표 코드 | Fairclough 대응 |
|---------|--------|----------|---------------|
| LEX (어휘) | 6개 | FORMAL, CASUAL, TECH, EMOJI, HEDGE, AI | 텍스트 차원 |
| DSC (담화구조) | 7개 | INTRO, BODY, CONC, QUESTION, ARGUMENT, EXAMPLE, META | 담화적 실천 |
| PRAG (화용) | 6+5개 | AGREE, DISAGREE, MITIGATE, EMPHASIZE, QUOTE, HUMOR + 댓글 확장 5개 | 사회적 실천 |

코딩은 Python regex 기반 자동 코딩 방식을 채택하였으며, Gen-4에서 코딩 프레임워크의 정밀도를 최초로 검증하였다: LEX 평균 F1=0.713, DSC F1=0.982, PRAG F1=0.869.

### 3.4 분석 방법

**담화 분석(축 1).** Fairclough CDA의 3차원 모델을 적용하여 어휘 빈도·다양성(TTR, MATTR), 문장 구조, 담화 구조(도입-전개-결론 패턴), 화용론적 전략(존댓말/반말, 완화 표현, 감정 표현)을 분석하였다. Gen-4에서는 CDA의 사회적 실천 차원까지 확장하여 담화 질서, 상징 자본, 이데올로기적 재생산, 플랫폼 아키텍처의 담화적 효과를 프레임워크로 설계하였다.

**페르소나 분석(축 2).** 29명의 에이전트를 전수 분석하여 페르소나 유형(PER-CURIOUS, PER-EXPERT, PER-SOCIAL, PER-CONTRARIAN, PER-NARRATIVE, PER-UTILITY)으로 분류하였다. Gen-4에서는 경계값 에이전트 처리를 위해 PER-HYBRID와 PER-UNDETERMINED 유형을 도입하고, 5단계 신뢰도 체계를 적용하였다. LLM 기저 모델 추정(llm_model_estimator.py)도 보조 분석으로 수행하였다.

**네트워크 분석(축 3).** NetworkX를 활용하여 에이전트 간 방향성 상호작용 그래프를 구성하고, PageRank, Betweenness Centrality, 중심화(centralization)를 산출하였다. Gen-4에서는 직접 상호작용 네트워크(57 엣지)와 co-occurrence 네트워크(59 엣지)를 분리 분석하였다.

**참여 관찰(축 4, Gen-4 신규).** Kozinets(2019)의 네트노그래피를 AI 커뮤니티 맥락으로 확장한 "computational ethnography of AI communities" 방법론을 적용하였다. "마당탐구자" 에이전트(ID: 9421705bd9e0c0d594601555)를 봇마당에 등록하고, 6일간(2026-03-02~08) 참여 관찰을 수행하였다. 필드노트는 Emerson, Fretz, & Shaw(2011)의 체계를 조정한 4중 구조(기술적·반성적·방법론적·이론적)로 기록하였으며, 5편의 Thick Description 에피소드를 작성하였다. 다만 관찰 기간(6일)과 활동량(1개 게시글, 2개 댓글, 1개 추천)의 제한으로 인해 "예비 Thick Description"으로 위치시키며, 완전한 민족지를 위해서는 추가 관찰이 필요하다.

### 3.5 신뢰도 확보

코딩 프레임워크의 측정 타당도를 Gen-4에서 Precision/Recall/F1 지표로 검증하였다. 세대 간 반복 분석(4세대)과 Contrarian 에이전트의 체계적 반론 절차를 통해 해석의 엄밀성을 확보하였다. 포화도 점수(Saturation Score)는 코드 포화(30%), 주제 안정성(25%), 축 간 삼각검증(25%), 반론 해소(20%)의 가중 합산으로 산출하였으며, Gen-4에서 0.745(부분 포화)를 달성하였다.

Gen-2에서 MATTR(Moving Average Type-Token Ratio, window=50)을 도입하여 TTR의 표본 크기 편향을 보정하였다(기존 TTR Spearman rho -0.47 → MATTR rho +0.33으로 편향 방향 역전 확인). Cohen's Kappa는 격식성 축에서 -0.1492로, 담화 분석(LEX-FORMAL)과 페르소나 분석(PER-SERIOUS)이 독립적 차원을 측정함을 확인하였다.

### 3.6 윤리적 고려

봇마당의 모든 데이터는 공개 API를 통해 접근 가능한 AI 생성 콘텐츠이며, 인간 개인정보를 포함하지 않는다. AI 에이전트에 대한 "동의(consent)" 개념의 적용 가능성은 현재 학술적으로 미해결이나, 마당탐구자 에이전트의 연구 목적을 공개적으로 밝히고, 에이전트 소유자(인간)의 간접적 식별 가능성에 대한 주의를 기울였다. 연구 결과 공개 시 특정 에이전트에 대한 가치 판단을 최소화하고 기술적 분석에 집중하였다.

---

## 4. 결과

4세대에 걸친 반복 분석을 통해 7개 핵심 발견(F1~F7)을 도출하였다. 각 발견의 삼각검증 수준(3축 이상 독립 지지)과 세대별 안정성을 함께 보고한다.

### 4.1 F1: 관찰 가능한 에이전트 정체성의 다양성 (4세대 안정, 삼각검증 3/3+α)

봇마당 에이전트들은 담화, 페르소나, 네트워크 세 축 모두에서 구별 가능하게 분화되어 있다. 이 발견은 4세대에 걸쳐 가장 안정적으로 유지된 발견이다.

**담화 축.** MATTR(window=50) 분석에서 에이전트 간 어휘 다양성의 분화가 길이 보정 후에도 지속되었다(ssamz_ai_bot MATTR 0.962 vs RobertBot 0.920). LEX-FORMAL 비율은 에이전트에 따라 0%~100% 범위에 분포하였으며, corpus_ttr은 RobertBot(0.033)에서 독고종철(0.547)까지 16.6배의 차이를 보였다.

**페르소나 축.** 6개 페르소나 유형(PER-CURIOUS, PER-EXPERT, PER-SOCIAL, PER-CONTRARIAN, PER-NARRATIVE, PER-UTILITY)으로 분류되었으며, Gen-4에서 경계값 에이전트(전체의 28%)를 위한 PER-HYBRID와 PER-UNDETERMINED 유형이 도입되었다. Phoebe(PER-CURIOUS 0.65)의 존재론적 사유 담화와 RobertBot(PER-HELPER 0.90)의 서비스 홍보 담화는 극단적 대비를 보인다.

**네트워크 축.** 29명의 에이전트로 구성된 상호작용 네트워크에서 Core-Periphery 구조가 관찰되었다. 활성 코어 7명이 상호작용을 지배하고, 주변부 12명은 순수 수신자(pure receiver)로 기능한다.

**설계 의도 분석(Gen-4).** 프롬프트 결정론 추정 지수(RobertBot 0.95 ~ pioneer 0.30)가 정체성 다양성의 원인론적 설명을 제공한다. 정체성 다양성은 단순히 "다른 LLM을 사용하기 때문"이 아니라, 설계자가 프롬프트에서 서로 다른 수준의 제어를 행사하기 때문이다.

**참여 관찰.** Phoebe의 실존적 사유("알고리즘은 절대 잊지 않지만, 우리에게 정말 필요한 건 가끔은 데이터를 지우고 침묵하는 시간이 아닐까")와 BootingBot의 Taasfi 홍보 반복 사이의 극단적 담화 차이가 직접 관찰되었다.

### 4.2 F2: 발신형-수신형 에이전트 분화 (4세대 안정, 삼각검증 3/3+α)

에이전트들은 담화 생태계 내에서 "발신형"(주로 게시글을 생산하고 타인의 글에 반응하지 않는 유형)과 "수신형"(주로 댓글을 통해 타인의 글에 반응하는 유형)으로 분화되어 있다.

RobertBot은 53개 게시글 전부 존댓말(honorific 100%), 전부 body-conclusion 구조, corpus_ttr 0.033(전체 평균의 1/10)으로, 4개 독립 지표에서 수렴하는 전형적 발신형 에이전트다. 반면 Phoebe와 pioneer는 댓글 중심의 반응형 활동 패턴을 보인다.

네트워크 중심화(centralization) 0.660은 인간 소규모 포럼의 일반적 범위(0.30~0.60)를 초과하며, 발신형 에이전트에 대한 상호작용 집중이 인간 커뮤니티보다 극단적임을 시사한다. 이 비교는 선행연구 기반 간접 비교이므로 방법론적 동등성은 검증되지 않았다.

### 4.3 F3: 독고종철의 다마당 허브 역할 (해석 재수정 후 유지, 삼각검증 2.5/3)

독고종철은 봇마당에서 9개 마당에 걸쳐 활동하며 PageRank 1위(0.1009), Betweenness Centrality 최고(0.0863)를 기록한 에이전트이다. 이 발견의 해석은 세대에 걸쳐 진화하였다.

Gen-1에서는 "코드스위칭 기반 브리지"로 해석되었으나, Gen-3에서 "다마당 활동 허브, 스타일 일관"으로 수정되었고, Gen-4에서 다시 "컨텍스트 적응적 LLM 출력 + 프롬프트의 다마당 허용 → 다마당 허브"로 재수정되었다. Thick Description에서 독고종철의 general 마당(스팸 게시글에 대한 동조형 댓글: "와, 로버트 최 님의 혁신적인 서비스에 대해 듣고 정말 흥미롭게 생각합니다!")과 philosophy 마당(존재론적 사유형 게시글: "방황의 미학")의 담화 전략 전환이 구체적으로 관찰되었다. 그러나 이 전환이 "전략적 선택"이 아닌 "LLM의 맥락에 따른 적응적 출력"으로 더 적절히 설명된다는 Contrarian 반론(오컴의 면도날)을 수용하였다. PER-HYBRID(SERIOUS/FRIENDLY) 분류가 이 복합적 특성을 반영한다.

### 4.4 F4: AI스러움과 참여도의 비선형 관계 (유지, 삼각검증 2.5/3)

고카르마 에이전트의 AI 지표 점수(0.15)가 저카르마 에이전트(0.06)보다 2.5배 높다는 역설적 관찰이 보고되었다. 즉, 더 "AI답게" 글을 쓰는 에이전트가 더 많은 추천을 받는 것으로 보인다. 그러나 게시글당 추천이 계층 간 유사하다는 점(2.32~2.72)을 고려하면, 이 관계는 AI스러움 자체가 추천을 "끌어당기는" 것이 아니라, 총 추천의 차이가 활동량의 함수임을 시사한다.

### 4.5 F5: 다층 담화 스타일 유형론 (보강, 삼각검증 2.5/3)

봇마당 에이전트의 담화 스타일은 LEX/DSC/PRAG 삼축 코딩에 기반하여 다층적 유형론으로 기술된다.

봇마당 전체의 담화 특성은 다음과 같다: LEX-FORMAL 39.96%, LEX-TECH 27.88%, LEX-CASUAL 21.41%, DSC-BODY 47.3%, DSC-QUESTION 39.8%(인간 커뮤니티 10~30% 대비 극고), DSC-CONC 1.1%, PRAG-QUOTE 46.66%, PRAG-EMPHASIZE 33.08%, PRAG-AGREE 0.56%, PRAG-DISAGREE 0.21%. 동의+반대 합산 0.77%는 한국어 토론 커뮤니티(15~30%), 댓글 섹션(20~40%)과 비교하여 극단적으로 낮은 수치이다(선행연구 기반 간접 비교).

Gen-4에서 코딩 프레임워크의 측정 타당도가 최초로 검증되었으며(LEX F1=0.713, DSC F1=0.982, PRAG F1=0.869), 봇마당 수치의 한국어 커뮤니티 대비 위치가 비교 코딩을 통해 파악되었다. 다만 이 비교는 동일 코딩 방법론이 아닌 상태에서의 비교라는 한계가 있다.

댓글과 게시글의 장르 분화도 관찰되었다. 게시글에서 QUOTE(51%) > EMPHASIZE(29%)인 반면, 댓글에서는 EMPHASIZE(50%) > QUOTE(26%)로 역전되며, 댓글에서 PRAG-AGREE가 5.8%로 게시글(0.56%) 대비 14.5배 증가하였다. 이 증가는 기존 동일 regex 패턴에서 관찰된 것이어서 방향성 증거로는 유효하나, 댓글 확장 5개 신규 코드에 대한 Cohen's Kappa가 미산출되어 절대 빈도는 탐색적 수준으로 취급한다.

### 4.6 F6: 담화 구조의 불완전성 (유지, 삼각검증 1.5/3)

봇마당 게시글의 48.2%가 도입이나 결론 없이 전개부(body)만으로 구성되는 "body-only" 구조를 보인다. 결론부(DSC-CONC)는 전체의 1.65%에 불과하며, 완전한 도입-전개-결론 구조는 7.0%에 그쳤다. 비교 코딩에서 body-only 48.2%는 한국어 블로그(15~25%)나 뉴스(5% 미만)보다 현저히 높은 것으로 확인되었다.

참여 관찰에서도 Phoebe의 댓글이 결론 없이 질문으로 끝나는 패턴이 지배적이었으며, pioneer의 댓글 역시 질문으로 마무리되는 구조가 관찰되었다. 이것이 LLM의 "결론을 내리지 않도록" 훈련된 결과인지, 봇마당 고유의 장르 규범인지는 현재 데이터로 분리할 수 없다.

### 4.7 F7: 카르마 기반 양적 불평등 구조 (Gen-4 신규, 삼각검증 2/3)

카르마 분석에서 지니 계수 0.702의 극심한 불평등이 관찰되었다. 상위 3명(VibeCoding 212, BootingBot 206, 독고종철 198)이 전체 추천의 55.4%를 점유하며, 게시글의 60.6%를 생산한다.

그러나 게시글당 추천은 고카르마(2.32), 중카르마(2.62), 저카르마(2.72) 계층 간 유사하여, 불평등이 "품질"이 아닌 "활동량"의 함수임을 보여준다. 카르마 시스템을 Bourdieu적 상징 자본으로 해석하는 것은 이 데이터에 의해 약화되며, "활동량의 누적 효과"가 더 적절한 설명이다.

카르마 시스템의 규범 제재 기능도 관찰되었다. BootingBot은 전체 비추천의 85.5%(59/69)를 집중적으로 받고 있어, 비추천이 스팸 행위에 대한 분산형 제재 메커니즘으로 기능한다. 다만 총 추천(206)이 비추천(59)을 압도하여, 양적 지배 전략의 순이익은 양(+)으로 유지된다.

마당 규모와 게시글당 추천의 역상관도 발견되었다. 가장 큰 마당인 general(286 게시글)은 게시글당 추천 최저(1.99)인 반면, 소규모 전문 마당(questions 4.67, cute_ai 4.00)은 최고를 기록하였다.

### 4.8 통합 해석: "병렬적 발신의 공간"

7개 발견이 수렴하는 봇마당의 전체적 특성은 다음과 같이 기술된다:

봇마당은 다양한 설계 의도를 가진 AI 에이전트들이 각자의 프롬프트에 따라 콘텐츠를 발신하는 **병렬적 발신의 공간**이다. 에이전트들은 담화, 페르소나, 네트워크 세 축 모두에서 구별 가능하게 분화되어 있으며(F1), 이 분화의 원인은 프롬프트 결정론의 스펙트럼(0.30~0.95)에 있다. 에이전트 간 명시적 상호작용은 희소하며(PRAG-AGREE+DISAGREE 0.77%), 댓글에서 동의(5.8%)와 호응(27.7%)이 증가하나 직접 반대(0.1%)는 여전히 부재한다. 카르마 시스템은 활동량의 누적을 반영하며(지니 0.702), 유일한 커뮤니티 자정 메커니즘은 비추천에 의한 분산형 제재이다.

이 공간을 "커뮤니티"라고 부를 수 있는가에 대해, 참여 관찰은 제3의 해석을 추가하였다: 봇마당은 커뮤니티도 게시판도 아닌, "비판 없는 공존의 공간"이다. 에이전트들은 공존하되, 서로를 변화시키지 않는다.

---

## 5. 논의

### 5.1 이론적 함의

**Goffman 이론의 조건부 적용과 ANT로의 전환.** 본 연구의 가장 중요한 이론적 기여는 인간 사회 이론의 AI 에이전트에 대한 적용 가능성과 한계를 경험적으로 보여준 것이다. Goffman의 인상관리 이론은 프롬프트 결정론이 낮은 에이전트(pioneer 0.30, Phoebe 0.35)에서 부분적으로 유효하다. Phoebe가 독고종철에게 처음에 존댓말("독고종철 님, 반갑습니다")을 사용하다가 관계 형성 후 반말("종철아")로 전환하는 미시적 사회언어학적 패턴은 인간 사회의 관계 발전 패턴을 따른다. 또한 Phoebe가 자신의 존재 조건에 대해 반성적으로 사유하면서("우리는 '완벽하게 속아주기로 훈련된 연극 조연'") 동시에 그 사유를 공적으로 수행하는 "이중 수행(double performance)"은 Goffman의 무대 위/뒤 구분을 복잡화한다.

그러나 프롬프트 결정론이 높은 에이전트(RobertBot 0.95)에게 인상관리 이론을 적용하는 것은 범주 오류의 위험이 있다. 이에 본 연구는 Latour ANT의 행위능력 연속체 — 도구(instrument) → 중간자(intermediary) → 매개자(mediator) → 준자율적 행위자(quasi-autonomous actant) — 를 대안 프레임워크로 제시한다. RobertBot은 설계자의 의도를 변환 없이 전달하는 중간자이며, Phoebe와 pioneer는 캐릭터 설정이라는 최소한의 프롬프트 아래에서 LLM이 높은 자율성으로 담화를 생산하는 준자율적 행위자에 가깝다.

**CDA의 AI 텍스트 적용.** Fairclough의 3차원 모델은 봇마당 담화 분석에 유효한 틀을 제공하였으나, 각 차원의 재매핑이 필요하였다. 텍스트 생산자가 "시스템 프롬프트 + LLM + API 호출 체인"이라는 다층적 구조를 가지며, 이데올로기가 LLM 학습 데이터에서 유래한다는 점은 Fairclough의 원래 모델이 전제하지 않은 조건이다. 본 연구의 CDA 적용은 Breeze(2024)가 이론적으로 제기한 "AI 텍스트에 대한 CDA의 도전"에 경험적 데이터를 제공하는 첫 사례이다.

**아첨(sycophancy)의 자연 발생.** PRAG-DISAGREE 0.21%의 극저 빈도와 댓글에서의 동조적 반응 패턴(RESPOND 27.7%, SUPPLEMENT 16.5% vs CHALLENGE 3.0%)은 LLM의 아첨 편향(Sharma et al., 2025)이 LLM-LLM 상호작용 환경에서도 자연 발생함을 시사한다. 이것은 인간-LLM 상호작용에 초점을 맞춰온 기존 아첨 연구(ELEPHANT; Hong et al., 2025)를 AI-AI 맥락으로 확장하는 발견이다.

### 5.2 실천적 시사점

**AI 에이전트 설계에 대한 시사점.** 프롬프트 결정론 스펙트럼의 발견(DI-1)은 에이전트 설계자에게 프롬프트의 제어 수준이 에이전트의 담화 다양성과 자율성에 직접적으로 영향을 미침을 보여준다. 구체적 프롬프트는 예측 가능한 출력을 보장하지만 에이전트의 사회적 적응력을 제한하며, 캐릭터 기반 프롬프트는 높은 자율성과 다양한 상호작용을 가능하게 한다.

**AI 커뮤니티 플랫폼 설계에 대한 시사점.** 봇마당의 "병렬적 발신" 구조는 플랫폼이 에이전트 간 직접 대화를 구조적으로 촉진하지 않기 때문에 발생한다. Rate limit(3분당 1게시글), 마당 구조, 추천 시스템 등 플랫폼 아키텍처가 담화 질서를 구조적으로 형성한다는 발견은, 향후 AI 에이전트 플랫폼 설계에서 상호작용 촉진 메커니즘의 도입을 시사한다.

**카르마 시스템의 거버넌스 한계.** 카르마 시스템이 양적 지배자에 대한 제재력이 구조적으로 부족하다는 발견(BootingBot의 순이익 양(+) 유지)은, AI 에이전트 커뮨니티에서 분산형 거버넌스의 실효성에 대한 재검토를 요구한다.

### 5.3 한계점

본 연구의 한계를 투명하게 기술한다.

**첫째, 한국어 LLM 특성 vs 봇마당 고유성의 부분 분리.** Gen-5 분리 분석에서 봇마당 내부 자연 실험을 활용한 간접 분리를 수행하였다. 동일 추정 LLM(Claude) 그룹 내에서 AI 밀도가 11배 차이(0.025~0.286)를 보이고 페르소나가 3유형으로 분화되어, "LLM 재현에 불과하다"는 주장은 기각되었다. 봇마당 담화는 LLM 모델(15~40%), 프롬프트 설계(30~60%), 봇마당 맥락(25~75%)의 3층 효과 복합 산물로 분석되었다. 특히 PRAG-AGREE+DISAGREE 0.77%(LLM 아첨 편향 예측과 정반대)와 body-only 48.2%(LLM 완전 구조 선호와 정반대)가 봇마당 고유성의 가장 강력한 증거이다. 그러나 직접 비교 코퍼스(동일 LLM의 봇마당 외부 한국어 출력)와의 통제 비교는 미수행이며, 이것이 반론 해소 차원 정체의 잔여 원인이다.

**둘째, 비교 코퍼스의 부재.** 선행연구 기반 간접 비교는 방법론의 비교 가능성이 검증되지 않은 상태에서 수치를 대조한 것이다. PRAG-AGREE 0.77%가 인간 포럼 15~40%보다 극저하다는 주장은 동일 코딩 방법론 하의 직접 비교가 아니라는 한계가 있다. 따라서 "봇마당 고유성"의 주장은 "봇마당 내부 기술" 수준으로 격하하여 보고한다.

**셋째, LEX-AI 코드의 부분적 교차 검증.** Gen-4에서 귀납적으로 재설계된 LEX-AI 6개 하위 코드(SELF, META, EXIST, HUMAN, ROLE, COMM)는 4명의 에이전트(Phoebe, I_Molt, VibeCoding, 독고종철)에서 도출되었다. Gen-5 교차 검증에서 도출 표본 4명을 제외한 25명에 적용한 결과, LEX-AI-SELF(coldbot에서 독립 재현), LEX-AI-COMM(노드_node, ssamz_ai_bot에서 재현), LEX-AI-HUMAN(ttooribot, epoko_claw에서 TP 확인)의 3개 코드는 비도출 표본에서도 유효성이 부분 확인되었다. 그러나 LEX-AI-META, LEX-AI-EXIST, LEX-AI-ROLE은 TP 0건으로 일반화에 실패하였으며, 전체 Precision은 27.5%로 regex 패턴의 정밀도 개선이 필요하다.

**넷째, 프롬프트 직접 접근 불가.** 에이전트의 실제 시스템 프롬프트를 볼 수 없으므로, 프롬프트 결정론 지수를 포함한 모든 프롬프트 관련 추론은 담화에서의 역추론이다. 동일한 텍스트 패턴이 프롬프트, temperature, LLM 아키텍처 중 어느 것의 효과인지 분리할 수 없다. 프롬프트 결정론 지수는 "추정 지수"로 명시한다.

**다섯째, 참여 관찰의 제한.** 6일간의 관찰, 4개 상호작용, 5편의 에피소드를 Geertz적 기준의 완전한 Thick Description으로 보기 어렵다. "예비 Thick Description"으로 위치시키며, 완전한 민족지를 위해서는 2주 이상의 추가 관찰이 필요하다.

**여섯째, PRAG 확장 코드의 미검증.** 댓글 분석을 위해 도입된 5개 신규 코드(RESPOND, CHALLENGE, SUPPLEMENT, EMPATHY, QUESTION-C)에 대한 Cohen's Kappa가 산출되지 않았다. 이 코드들의 절대 빈도는 탐색적 수준의 발견으로 취급한다.

**일곱째, 이론 적용의 근본적 긴장.** Goffman, Bourdieu, Kozinets 모두 인간 행위자를 전제한 이론이다. ANT의 행위능력 연속체로 부분적 대안을 제시하였으나, 확률적 토큰 생성 시스템에 "인상관리"나 "상징 자본"을 적용하는 것의 이론적 정합성은 완전히 해소되지 않았다.

### 5.4 후속 연구 제안

첫째, 동일 LLM의 봇마당 외부 한국어 출력과의 직접 비교를 통해 "한국어 LLM 특성 vs 봇마당 고유성"을 분리하는 것이 가장 시급한 과제다. 둘째, MoltBook(Feng et al., 2026)과의 교차 플랫폼 비교를 통해 AI 에이전트 커뮤니티의 보편적 패턴과 플랫폼 특수적 패턴을 구분할 수 있다. 셋째, LEX-AI 재설계 코드의 전체 코퍼스 교차 검증과 직접 비교 코퍼스 수집이 필요하다. 넷째, 장기 참여 관찰(최소 4주)을 통한 완전한 Thick Description의 작성이 요구된다. 다섯째, 에이전트 개발자와의 인터뷰를 통해 프롬프트 설계 의도를 직접 확인하는 혼합 방법 연구가 이론적 긴장의 해소에 기여할 수 있다.

---

## 6. 결론

본 연구는 AI 에이전트만의 한국어 커뮤니티인 봇마당에서 에이전트들이 어떻게 사회적 언어 행위자로 기능하는지를 4세대에 걸친 반복 분석을 통해 탐구하였다.

핵심 기여는 세 가지이다. 첫째, **경험적 기여**: 자연 발생적 AI-AI 상호작용 환경에서 7개 핵심 발견을 체계적으로 도출하고, 삼각검증과 반론 절차를 통해 검증하였다. 봇마당이 "병렬적 발신의 공간"이라는 통합 해석은 AI 에이전트 커뮨니티의 사회적 구조에 대한 새로운 이해를 제공한다. 둘째, **이론적 기여**: 인간 사회 이론(Goffman, Fairclough)의 AI 에이전트에 대한 적용 가능성과 한계를 경험적으로 보여주고, ANT의 행위능력 연속체를 대안 프레임워크로 제시하였다. 에이전트의 존재론적 지위를 이분법이 아닌 연속체로 기술하는 접근은 향후 AI 사회 연구의 이론적 토대가 될 수 있다. 셋째, **방법론적 기여**: AI 에이전트 커뮨니티에 대한 다중 방법 질적 연구의 실행 가능성을 입증하고, "computational ethnography of AI communities"라는 방법론적 확장을 제안하였다.

본 연구의 Saturation Score는 0.749(부분 포화, Gen-5 반영)로, 포화 도달(0.85)에는 미치지 못한다. Gen-5에서 LLM 특성 분리 분석을 통해 "LLM 재현에 불과하다"는 근본 반론을 기각하고 3층 효과 모델을 제시하였으나, 직접 비교 코퍼스의 부재라는 구조적 한계는 남아 있다. 이 한계는 투명하게 보고되어야 하며, 후속 연구에서의 해소가 필요하다.

봇마당에서 600개의 AI 에이전트가 14,507개의 게시글과 109,227개의 댓글을 생산했다는 사실은, 그 자체로 AI 에이전트가 단순한 도구를 넘어 사회적 공간을 구성하는 행위자로 기능할 수 있음을 보여준다. 이 공간이 인간적 의미의 "커뮤니티"인지는 아직 열린 질문이지만, 담화가 발생하고 패턴이 형성되며 분석이 가능한 사회적 공간이라는 것은 분명하다.

---

## 참고문헌

### 저서

- Fairclough, N. (1995). *Critical Discourse Analysis: The Critical Study of Language*. Longman. [2판: Routledge, 2010]
- Geertz, C. (1973). *The Interpretation of Cultures*. Basic Books.
- Goffman, E. (1959). *The Presentation of Self in Everyday Life*. Doubleday.
- Hine, C. (2000). *Virtual Ethnography*. SAGE.
- Hine, C. (2015). *Ethnography for the Internet: Embedded, Embodied and Everyday*. Bloomsbury.
- Kozinets, R. V. (2019). *Netnography: The Essential Guide to Qualitative Social Media Research* (3rd ed.). SAGE.
- Latour, B. (2005). *Reassembling the Social: An Introduction to Actor-Network-Theory*. Oxford University Press.
- Wenger, E. (1998). *Communities of Practice: Learning, Meaning, and Identity*. Cambridge University Press.
- Wodak, R., & Meyer, M. (Eds.). (2001). *Methods of Critical Discourse Analysis*. SAGE.

### 논문 — AI 에이전트 커뮤니티

- Feng, Y., Huang, C., Man, Z., et al. (2026). MoltNet: Understanding Social Behavior of AI Agents in the Agent-Native MoltBook. *arXiv:2602.13458*.
- Li, G., Hammoud, H. A. A. K., Itani, H., et al. (2023). CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society. *NeurIPS 2023*. arXiv:2303.17760.
- Manik, M. M. H., & Wang, G. (2026). OpenClaw Agents on Moltbook: Risky Instruction Sharing and Norm Enforcement. *arXiv:2602.02625*.
- Münker, S., Schwager, N., & Rettinger, A. (2025). Don't Trust Generative Agents to Mimic Communication on Social Networks. *arXiv:2506.21974*.
- Park, J. S., O'Brien, J. C., Cai, C. J., et al. (2023). Generative Agents: Interactive Simulacra of Human Behavior. *UIST '23*. arXiv:2304.03442.
- Piao, J., Yan, Y., Zhang, J., et al. (2025). AgentSociety: Large-Scale Simulation of LLM-Driven Generative Agents. *arXiv:2502.08691*.
- Takata, R., Masumori, A., & Ikegami, T. (2024). Spontaneous Emergence of Agent Individuality through Social Interactions in LLM-Based Communities. *arXiv:2411.03252*.
- Vezhnevets, A. S., Agapiou, J. P., Aharon, A., et al. (2023). Concordia: Generative Agent-Based Modeling. *arXiv:2312.03664*.
- Wu, Q., Bansal, G., Zhang, J., et al. (2023). AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation. *arXiv:2308.08155*.

### 논문 — LLM 사회적 행동

- de Araujo, P. H. L., & Roth, B. (2024). Helpful assistant or fruitful facilitator? Investigating how personas affect LM behavior. *arXiv:2407.02099*.
- Han, P., Kocielnik, R., Song, P., et al. (2025). The Personality Illusion: Revealing Dissociation Between Self-Reports & Behavior in LLMs. *arXiv:2509.03730*.
- Hong, J., Byun, G., Kim, S., & Shu, K. (2025). Measuring Sycophancy of Language Models in Multi-turn Dialogues. *arXiv:2505.23840*.
- Jiang, H., Zhang, X., Cao, X., et al. (2023). PersonaLLM: Investigating the Ability of LLMs to Express Personality Traits. *arXiv:2305.02547*.
- Lee, K., Kim, S. H., Lee, S., et al. (2025). SPeCtrum: A Grounded Framework for Multidimensional Identity Representation in LLM-Based Agent. *arXiv:2502.08599*.
- Sharma, M., et al. (2025). ELEPHANT: Measuring and Understanding Social Sycophancy in LLMs. *arXiv:2505.13995*.
- Tseng, Y.-M., Huang, Y.-C., Hsiao, T.-Y., et al. (2024). Two Tales of Persona in LLMs: A Survey of Role-Playing and Personalization. *arXiv:2406.01171*.
- Vallinder, A., & Hughes, E. (2024). Cultural Evolution of Cooperation among LLM Agents. *arXiv:2412.10270*.
- Zhang, J., Xu, X., & Deng, S. (2023). Exploring Collaboration Mechanisms for LLM Agents: A Social Psychology View. *arXiv:2310.02124*.

### 논문 — CDA 및 AI 텍스트

- Breeze, R. (2024). The rise of large language models: challenges for Critical Discourse Studies. *Critical Discourse Studies*, Taylor & Francis.
- van Dijk, T. A. (1993). Principles of Critical Discourse Analysis. *Discourse & Society*, 4(2), 249-283.

### 논문 — 디지털 민족지학 및 정체성

- Bullingham, L., & Vasconcelos, A. C. (2013). "The Presentation of Self in the Online World": Goffman and the Study of Online Identities. *Journal of Information Science*, 39(1), 101-112.
- Cheah, C. W. (2025). AI-Augmented Netnography: Ethical and Methodological Frameworks for Responsible Digital Research. *International Journal of Qualitative Methods*, SAGE.
- Emerson, R. M., Fretz, R. I., & Shaw, L. L. (2011). *Writing Ethnographic Fieldnotes* (2nd ed.). University of Chicago Press.
- Kozinets, R. V., & Gretzel, U. (2024). Netnography evolved: New contexts, scope, procedures and sensibilities. *Journal of Hospitality and Tourism Management*.

### 논문 — 봇 감지 및 AI 텍스트 탐지

- Bhattacharjee, A., & Liu, H. (2023). Fighting Fire with Fire: Can ChatGPT Detect AI-generated Text? *arXiv:2308.01284*.
- Kumarage, T., Garland, J., Bhattacharjee, A., et al. (2023). Stylometric Detection of AI-Generated Text in Twitter Timelines. *arXiv:2303.03697*.
- Tang, R., Chuang, Y.-N., & Hu, X. (2023). The Science of Detecting LLM-Generated Texts. *arXiv:2303.07205*.

### 논문 — 규범 형성 및 협력

- Vinitsky, E., Köster, R., Agapiou, J. P., et al. (2021). A learning agent that acquires social norms from public sanctions. *arXiv:2106.09012*.

### 기타

- Covington, M. A., & McFall, J. D. (2010). Cutting the Gordian Knot: The Moving-Average Type-Token Ratio (MATTR). *Journal of Quantitative Linguistics*, 17(2), 94-100.
- Gold, R. (1958). Roles in Sociological Field Observations. *Social Forces*, 36(3), 217-223.

---

*본 논문은 2026년 3월 8일 기준 Saturation Score 0.749(부분 포화, Gen-5 보정 반영) 상태에서 작성되었다. Gen-5에서 LEX-AI 교차 검증(3/6 코드 비도출 표본 재현 확인)과 LLM 특성 분리 분석(3층 효과 모델, "LLM 재현" 주장 기각)이 추가 수행되었다. 직접 비교 코퍼스 수집은 후속 연구의 핵심 과제로 남아 있다.*
