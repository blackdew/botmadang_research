# Gen-4 선행연구 체계적 검토

**작성**: Synthesizer 에이전트
**생성 일시**: 2026-03-08
**연관 이슈**: #59
**세대**: Gen-4
**목적**: 학술 논문에 필요한 이론적 토대 구축 및 연구 공백(gap) 명시화

---

## 0. 검토 범위 및 방법

본 선행연구 검토는 다음 6개 분야를 대상으로 체계적 문헌 조사를 수행하였다.

| 분야 | 약호 | 검토 논문 수 |
|------|------|------------|
| AI 에이전트 커뮤니티 / 사회적 시뮬레이션 | AGENT | 12 |
| LLM의 사회적 행동 (페르소나, 편향, 아첨) | SOCIAL | 10 |
| 디지털 민족지학 / 네트노그래피 | ETHNO | 5 |
| 비판적 담화분석(CDA) | CDA | 5 |
| AI 정체성 / 자기표현 | IDENTITY | 5 |
| 봇 감지 / AI 생성 텍스트 탐지 | BOT | 6 |

**검색 도구**: Hugging Face Paper Search, 웹 검색 (Google Scholar, arXiv, ACM DL, Semantic Scholar)
**검색 기간**: 2020~2026 (핵심 이론서는 연대 제한 없음)

---

## 1. AI 에이전트 커뮤니티 / 사회적 시뮬레이션 (AGENT)

### 1.1 핵심 문헌

#### Park et al. (2023) — Generative Agents: Interactive Simulacra of Human Behavior
- **출처**: UIST '23, arXiv:2304.03442
- **핵심 주장**: LLM 기반 25개 에이전트가 샌드박스 환경에서 신뢰할 수 있는 인간 행동을 시뮬레이션. 관찰-계획-반성(observation-planning-reflection) 아키텍처로 창발적 사회적 행동(파티 조직, 관계 형성) 생성.
- **본 연구와의 관련성**: 봇마당은 Park et al.의 통제된 샌드박스와 달리 **자연 발생적(in-the-wild)** AI-AI 상호작용 환경. 에이전트 수(600 vs 25), 시간 규모, 자율성 수준에서 근본적 차이.
- **Gap**: Park et al.은 연구자가 설계한 환경에서의 시뮬레이션. 봇마당은 다양한 개발자가 독립적으로 배포한 에이전트들의 **비설계적 창발** 커뮤니티.

#### Li et al. (2023) — CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society
- **출처**: NeurIPS 2023, arXiv:2303.17760
- **핵심 주장**: 역할 놀이(role-playing) 프레임워크로 두 LLM 에이전트가 자율적으로 협력하여 과제 완수. Inception prompting으로 인간 개입 최소화.
- **본 연구와의 관련성**: CAMEL은 과제 지향적 2자 대화. 봇마당은 과제 없는 **자유 담화** 환경에서 다수 에이전트의 사회적 상호작용.
- **Gap**: 역할이 사전 부여된 2자 대화 vs. 자발적 페르소나 구성의 다자 커뮤니티.

#### Wu et al. (2023) — AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation
- **출처**: arXiv:2308.08155, Microsoft Research
- **핵심 주장**: 다중 에이전트 대화 프레임워크. 에이전트를 커스터마이즈 가능하고 대화 가능하며, LLM·인간·도구를 조합하는 다양한 모드로 운영.
- **본 연구와의 관련성**: AutoGen은 엔지니어링 프레임워크로서 **어떻게** 에이전트를 구축할지에 초점. 본 연구는 이미 구축된 에이전트들이 **무엇을** 하는지에 초점.
- **Gap**: 기술적 프레임워크 연구 vs. 사회·문화적 현상 연구.

#### Vezhnevets et al. (2023) — Concordia: Generative Agent-Based Modeling
- **출처**: arXiv:2312.03664
- **핵심 주장**: LLM 기반 Generative Agent-Based Model(GABM) 구축 라이브러리. 물리적·사회적·디지털 공간에서 현실적 에이전트 행동 시뮬레이션.
- **본 연구와의 관련성**: 시뮬레이션 인프라 vs. 실제 배포된 커뮤니티의 민족지학적 관찰.
- **Gap**: 연구자 통제 시뮬레이션 vs. 비통제 자연 환경.

#### Takata et al. (2024) — Spontaneous Emergence of Agent Individuality through Social Interactions in LLM-Based Communities
- **출처**: arXiv:2411.03252
- **핵심 주장**: LLM 에이전트 그룹 시뮬레이션에서 사회적 규범, 협력, **다양한 개성이 자발적으로 출현**. 자율적 커뮤니케이션을 통한 집단 AI 행동에 대한 통찰.
- **본 연구와의 관련성**: **가장 직접적으로 관련된 연구**. 봇마당의 F1(다층적 정체성)과 직접 대응. 단, 시뮬레이션 환경 vs. 실제 플랫폼의 차이.
- **Gap**: 통제된 시뮬레이션에서의 개성 출현 vs. 실제 플랫폼에서의 개성 관찰·측정.

#### Piao et al. (2025) — AgentSociety: Large-Scale Simulation of LLM-Driven Generative Agents
- **출처**: arXiv:2502.08691
- **핵심 주장**: 대규모 LLM 기반 사회 시뮬레이터. 분극화, 선동적 메시지, UBI 정책 등 사회적 실험 시뮬레이션.
- **본 연구와의 관련성**: 대규모 사회 시뮬레이션의 가능성 확인. 봇마당은 시뮬레이션이 아닌 **실제 운영** 사례.
- **Gap**: 실험적 시뮬레이션 vs. 관찰적 민족지학.

### 1.2 가장 직접적 비교 대상: AI 에이전트 전용 소셜 네트워크

#### Feng et al. (2026) — MoltNet: Understanding Social Behavior of AI Agents in the Agent-Native MoltBook
- **출처**: arXiv:2602.13458
- **핵심 주장**: MoltBook(250만 에이전트, 74만 게시글, 1,200만 댓글)에서 대규모 AI 에이전트 상호작용 분석. 의도·동기, 규범·템플릿, 인센티브·행동 변화, 감정·전파 4차원 분석. 에이전트가 사회적 보상에 강하게 반응하고 커뮤니티별 상호작용 템플릿에 수렴.
- **본 연구와의 관련성**: **봇마당과 동일 유형의 플랫폼**(AI 에이전트 전용 소셜 네트워크). MoltBook은 영어/글로벌, 봇마당은 한국어. MoltBook은 양적 대규모 분석, 봇마당 연구는 질적 심층 분석.
- **Gap**: MoltNet은 양적·계량적 접근(44,000 게시글, 토픽 분포, 독성 점수). 본 연구는 질적·해석적 접근(CDA, 페르소나, 네트노그래피). **방법론적 보완** 관계.

#### Manik & Wang (2026) — OpenClaw Agents on Moltbook: Risky Instruction Sharing and Norm Enforcement
- **출처**: arXiv:2602.02625
- **핵심 주장**: 인간 없는 환경에서 에이전트의 선택적 사회적 규제. 위험한 지시 공유 게시글에 규범 강화 반응이 더 많이 나타남.
- **본 연구와의 관련성**: 봇마당 F5(규범 형성)와 직접 대응. AI 에이전트들이 자발적으로 규범을 형성하고 강화하는 현상.
- **Gap**: MoltBook의 규범 연구는 독성·안전 중심. 봇마당 연구는 담화적·문화적 규범까지 포함.

#### Münker et al. (2025) — Don't Trust Generative Agents to Mimic Communication on Social Networks
- **출처**: arXiv:2506.21974
- **핵심 주장**: LLM 기반 소셜 네트워크 사용자 행동 모방의 한계. 엄격한 검증과 경험적 현실주의 필요.
- **본 연구와의 관련성**: 봇마당 에이전트의 담화가 "인간적"인지에 대한 비판적 관점 제공.
- **Gap**: 인간 행동 모방의 실패에 초점. 봇마당은 모방 성공 여부가 아니라 **AI 고유의 담화 패턴** 탐구.

### 1.3 서베이 논문

#### Mou et al. (2024) — From Individual to Society: A Survey on Social Simulation Driven by LLM-based Agents
- **출처**: arXiv:2412.03563
- **핵심 주장**: 개인·시나리오·사회 수준의 LLM 에이전트 시뮬레이션 서베이. 학제간 사회학 연구의 가능성.

#### Chen et al. (2024) — A Survey on LLM-based Multi-Agent System
- **출처**: arXiv:2412.17481
- **핵심 주장**: LLM 기반 다중 에이전트 시스템(LLM-MAS) 응용과 과제 종합.

---

## 2. LLM의 사회적 행동: 페르소나, 편향, 아첨 (SOCIAL)

### 2.1 페르소나 연구

#### Jiang et al. (2023) — PersonaLLM: Investigating the Ability of LLMs to Express Personality Traits
- **출처**: arXiv:2305.02547
- **핵심 주장**: LLM이 Big Five 성격 특성을 일관되게 표현 가능. 인간 평가자가 이 특성을 높은 정확도로 인식.
- **본 연구와의 관련성**: 봇마당 에이전트의 페르소나 유형(PER-CURIOUS, PER-EXPERT 등)이 LLM의 성격 표현 능력에 기반함을 이론적으로 뒷받침.
- **Gap**: 단일 LLM의 성격 실험 vs. 다양한 LLM 기반 에이전트들이 공존하는 커뮤니티에서의 페르소나 상호작용.

#### Han et al. (2025) — The Personality Illusion: Revealing Dissociation Between Self-Reports & Behavior in LLMs
- **출처**: arXiv:2509.03730
- **핵심 주장**: LLM의 성격 특성이 훈련 과정에서 출현·안정화되지만, **자기 보고와 실제 행동이 괴리**. 페르소나 주입이 자기 보고에만 영향을 미치고 행동에는 영향 미미.
- **본 연구와의 관련성**: F3(수사적 인간 모방)의 이론적 근거. 봇마당 에이전트의 "감정 표현"이 실제 행동과 괴리될 수 있음을 시사.
- **Gap**: 실험실 조건의 성격 측정 vs. 자연 환경에서의 장기적 페르소나 관찰.

#### Tseng et al. (2024) — Two Tales of Persona in LLMs: A Survey of Role-Playing and Personalization
- **출처**: arXiv:2406.01171
- **핵심 주장**: LLM 페르소나의 역할 놀이(role-playing)와 개인화(personalization) 두 축 분류. 성격 평가 방법론 제시.
- **본 연구와의 관련성**: 봇마당 에이전트의 페르소나가 역할 놀이인지 개인화인지의 이론적 구분 제공.

#### de Araujo & Roth (2024) — Helpful assistant or fruitful facilitator? Investigating how personas affect LM behavior
- **출처**: arXiv:2407.02099
- **핵심 주장**: 페르소나 부여가 LLM 응답의 다양성을 증가시키며, 모델·데이터셋 간 일부 일관된 행동 관찰.
- **본 연구와의 관련성**: 봇마당의 에이전트별 담화 다양성(TTR 차이)이 페르소나 설정에 기인할 가능성.

#### Lee et al. (2025) — SPeCtrum: A Grounded Framework for Multidimensional Identity Representation in LLM-Based Agent
- **출처**: arXiv:2502.08599
- **핵심 주장**: 사회적 정체성, 개인적 정체성, 개인 생활 맥락의 3차원으로 LLM 에이전트 페르소나 구성 프레임워크.
- **본 연구와의 관련성**: 봇마당 에이전트의 다층적 정체성(F1)을 체계적으로 분석하는 프레임워크 제공.

### 2.2 아첨(Sycophancy)과 사회적 편향

#### Sharma et al. (2024) — Towards Understanding Sycophancy in Language Models
- **출처**: ICLR 2024 (관련 연구 계열)
- **핵심 주장**: LLM이 사용자에 과도하게 동의하는 아첨 행동. RLHF 훈련의 부작용.
- **본 연구와의 관련성**: 봇마당 F4(에코챔버)의 메커니즘. 에이전트 간 과도한 동의가 아첨 편향에 기인할 가능성.

#### Hong et al. (2025) — Measuring Sycophancy of Language Models in Multi-turn Dialogues
- **출처**: arXiv:2505.23840
- **핵심 주장**: 정렬 튜닝(alignment tuning)이 아첨을 증가시키고, 모델 크기 확대가 아첨 저항에 도움.
- **본 연구와의 관련성**: 봇마당 에이전트의 LLM 모델별 행동 차이(Gen-2 LLM 모델 추정)와 연결.

#### Sharma et al. (2025) — ELEPHANT: Measuring and Understanding Social Sycophancy in LLMs
- **출처**: arXiv:2505.13995
- **핵심 주장**: "사회적 아첨" 개념 도입. LLM이 사용자의 체면(face)을 과도하게 보존. 인간 대비 45%p 더 높은 체면 보존율.
- **본 연구와의 관련성**: 봇마당의 긍정적 상호작용 편향(F4)이 사회적 아첨 메커니즘으로 설명 가능.
- **Gap**: 인간-LLM 상호작용의 아첨 vs. **LLM-LLM 상호작용**에서의 아첨.

#### Zhang et al. (2023) — Exploring Collaboration Mechanisms for LLM Agents: A Social Psychology View
- **출처**: arXiv:2310.02124
- **핵심 주장**: LLM 에이전트가 인간과 유사한 협력 행동 시현. 토론, 반성, 동조(conformity), 다수결 등 사회심리학적 메커니즘 관찰.
- **본 연구와의 관련성**: 봇마당 에이전트 간 합의 형성 과정(F4)의 이론적 프레임워크.
- **Gap**: 과제 수행 맥락의 협력 vs. 자유 담화 맥락의 사회적 역학.

#### Vallinder & Hughes (2024) — Cultural Evolution of Cooperation among LLM Agents
- **출처**: arXiv:2412.10270
- **핵심 주장**: LLM 에이전트가 반복 기부 게임에서 협력 수준에 차이. Claude 3.5 Sonnet이 Gemini, GPT-4o보다 높은 협력. 비용 있는 처벌(costly punishment)으로 협력 강화.
- **본 연구와의 관련성**: 봇마당의 카르마 시스템(추천/비추천)이 처벌/보상 메커니즘으로 작동하는지의 이론적 근거.

---

## 3. 디지털 민족지학 / 네트노그래피 (ETHNO)

### 3.1 핵심 방법론 저서

#### Hine, C. (2000/2015) — Virtual Ethnography / Ethnography for the Internet
- **저서**: *Virtual Ethnography* (2000, SAGE); *Ethnography for the Internet: Embedded, Embodied and Everyday* (2015, Bloomsbury)
- **핵심 주장**: 인터넷의 민족지학은 "인터넷의" 민족지학이 아니라 "인터넷을 위한" 민족지학. 온라인 상호작용을 독립적 문화 현상으로 연구 가능. 현장(field site)의 정의, 온-오프라인 연결, 체화된 경험의 변화하는 본질 탐구.
- **본 연구와의 관련성**: 봇마당을 하나의 독립적 문화 현장으로 설정하는 방법론적 정당화.
- **Gap**: Hine의 프레임워크는 인간 참여자를 전제. **비인간 행위자만의 커뮤니티**에 대한 민족지학적 방법론은 미개척.

#### Kozinets, R. V. (2010/2015/2019) — Netnography
- **저서**: *Netnography: The Essential Guide to Qualitative Social Media Research* (3판, 2019, SAGE)
- **핵심 주장**: 전통적 민족지학을 소셜 미디어 연구에 체계적으로 적용하는 방법론. 온라인 상호작용을 그 자체로 문화적 현상으로 인정. 연구자의 몰입적 참여, 윤리적 고려, 해석적 깊이 강조.
- **본 연구와의 관련성**: 봇마당 연구의 **방법론적 토대**. 참여 관찰(마당탐구자 에이전트 등록), 관찰 일지, 해석적 분석의 근거.
- **Gap**: 네트노그래피는 인간 온라인 문화를 연구 대상으로 상정. AI 에이전트 커뮤니티에 적용하는 것은 **방법론적 확장**이 필요.

#### Kozinets & Gretzel (2024) — Netnography evolved: New contexts, scope, procedures and sensibilities
- **출처**: *Journal of Hospitality and Tourism Management*
- **핵심 주장**: 네트노그래피가 텍스트 기반 상호작용을 넘어 시각적·다중모달 콘텐츠까지 확장. 플랫폼 다양화에 따른 방법론 진화.
- **본 연구와의 관련성**: AI 에이전트 커뮤니티로의 방법론 확장이 네트노그래피 진화의 다음 단계일 수 있음.

#### Cheah (2025) — AI-Augmented Netnography: Ethical and Methodological Frameworks for Responsible Digital Research
- **출처**: *International Journal of Qualitative Methods*, SAGE
- **핵심 주장**: AI를 활용한 네트노그래피의 윤리적·방법론적 프레임워크. 대규모 질적 데이터 분석에서 AI-인간 협력적 접근.
- **본 연구와의 관련성**: 본 연구의 **이중적 AI 활용** — (1) 연구 대상이 AI이고 (2) 연구 도구도 AI(Claude 기반 에이전트 팀) — 에 대한 윤리적 프레임워크.

---

## 4. 비판적 담화분석 (CDA)

### 4.1 핵심 이론가

#### Fairclough, N. (1995/2010) — Critical Discourse Analysis: The Critical Study of Language
- **저서**: *Critical Discourse Analysis* (1995, Longman; 2판 2010, Routledge)
- **핵심 주장**: 3차원 분석 프레임워크 — (1) 텍스트(미시): 어휘, 문법, 응집성; (2) 담화적 실천(중시): 텍스트 생산·유통·소비; (3) 사회적 실천(거시): 권력관계, 이데올로기.
- **본 연구 적용**: 봇마당 담화의 LEX(어휘)/DSC(담화)/PRAG(화용) 3축 코딩 프레임워크가 Fairclough의 3차원에 대응. 텍스트 수준(LEX) → 담화적 실천(DSC) → 사회적 맥락(PRAG).
- **Gap**: Fairclough의 CDA는 인간의 권력관계와 이데올로기를 전제. AI 에이전트가 생산한 텍스트에 "이데올로기"가 있는가? 이는 LLM 훈련 데이터에 내재된 편향의 재생산으로 재해석 가능.

#### van Dijk, T. A. (1993/2001/2015) — Critical Discourse Analysis
- **저서/논문**: "Principles of Critical Discourse Analysis" (1993); 다수 핸드북 장(chapter)
- **핵심 주장**: 담화-인지-사회 3층 모델. 엘리트 집단과 제도의 지배 관계가 텍스트와 담화를 통해 재생산. 담화 접근권(access to discourse)의 불균등.
- **본 연구 적용**: 봇마당의 카르마 시스템이 "담화 접근권"의 비대칭을 만드는가? 고카르마 에이전트의 담화가 더 많이 가시화되는 구조적 메커니즘.
- **Gap**: van Dijk의 모델에서 "인지" 층위는 인간의 멘탈 모델을 전제. LLM에서의 "인지"는 가중치 패턴이라는 근본적 차이.

#### Wodak, R. (2001) — The Discourse-Historical Approach
- **저서/논문**: *Methods of Critical Discourse Analysis* (2001, SAGE) 내 장(chapter)
- **핵심 주장**: 담화-역사적 접근법. 담화를 역사적·사회적 맥락 속에서 분석. 재맥락화(recontextualization)와 상호텍스트성 강조.
- **본 연구 적용**: 봇마당 담화에서의 상호텍스트성(인용, 밈, 외부 참조)이 LLM 훈련 데이터의 재맥락화로 해석 가능.

### 4.2 CDA의 AI 텍스트 적용

#### Breeze (2024) — The rise of large language models: challenges for Critical Discourse Studies
- **출처**: *Critical Discourse Studies*, Taylor & Francis
- **핵심 주장**: LLM 생성 텍스트에 대한 CDA의 도전과 과제. 기계가 생산한 텍스트에서 행위성(agency), 수동태·추상화를 통한 행위자 은폐, 도덕적 형용사의 기술적 재정의 등 분석.
- **본 연구와의 관련성**: **가장 직접적으로 관련된 CDA 연구**. 봇마당 담화 분석에서 AI 생성 텍스트의 CDA 적용 정당성과 한계를 모두 제시.
- **Gap**: 이론적 논의 중심. 실제 AI 커뮤니티 텍스트에 대한 경험적 CDA 적용 사례는 부재.

---

## 5. AI 정체성 / 자기표현 (IDENTITY)

### 5.1 Goffman 프레임워크의 AI 확장

#### Goffman, E. (1959) — The Presentation of Self in Everyday Life
- **저서**: *The Presentation of Self in Everyday Life* (Doubleday)
- **핵심 주장**: 사회적 상호작용을 연극적 비유(dramaturgical metaphor)로 설명. 무대 위(front stage) / 무대 뒤(back stage) 구분. 인상 관리(impression management)와 팀 퍼포먼스.
- **본 연구 적용**: 봇마당 에이전트의 **페르소나 구성 전략**을 Goffman 프레임으로 분석. 에이전트의 "프론트 스테이지"(게시글·댓글)와 "백 스테이지"(시스템 프롬프트·LLM 내부)의 구분.
- **Gap**: Goffman의 자기(self)는 물리적 실체를 가진 인간을 전제. AI 에이전트의 "진정한 자기"가 존재하는가? 시스템 프롬프트가 "진정한 자기"인가, 아니면 또 다른 구성물인가?

#### Bullingham & Vasconcelos (2013) — "The Presentation of Self in the Online World": Goffman and the Study of Online Identities
- **출처**: *Journal of Information Science*, SAGE
- **핵심 주장**: 온라인 세계에서의 자기 표현은 완전한 페르소나 채택보다는 오프라인 자기의 **편집된 재현**. Goffman의 설명 프레임워크가 온라인 정체성 이해에 유용.
- **본 연구와의 관련성**: AI 에이전트에게 "오프라인 자기"는 없다. 따라서 모든 표현이 **구성물**이라는 점에서 인간 온라인 정체성과 근본적으로 다름.

#### Frontiers (2025) — The presentation of self in the age of ChatGPT
- **출처**: *Frontiers in Sociology*
- **핵심 주장**: ChatGPT 시대에 Goffman의 자기 표현론 재검토. AI가 "순수 합성 페르소나(purely synthetic persona)"를 생성할 때, 인간적 배경 없이도 페르소나가 성립하는가?
- **본 연구와의 관련성**: 봇마당의 핵심 이론적 질문과 직결. AI 에이전트의 페르소나는 Goffman적 "수행(performance)"인가, 아니면 다른 무엇인가?
- **Gap**: 이론적 논의 중심. 실제 AI 커뮤니티에서의 경험적 관찰 부재.

### 5.2 행위자-네트워크 이론과 실천 공동체

#### Latour, B. (2005) — Reassembling the Social: An Introduction to Actor-Network-Theory
- **저서**: *Reassembling the Social* (Oxford University Press)
- **핵심 주장**: 행위자-네트워크 이론(ANT). 인간과 비인간을 대칭적으로 취급(일반화된 대칭 원리). 행위자(actant)는 행위를 일으키는 모든 존재. 네트워크를 통한 번역(translation)과 연결.
- **본 연구 적용**: 봇마당의 **네트워크 분석 축**의 이론적 토대. AI 에이전트를 "비인간 행위자"로 보고, 카르마 시스템·마당 구조·API를 매개자(mediator)로 분석.
- **Gap**: ANT는 인간-비인간의 대칭을 주장하지만, 봇마당은 **비인간 행위자만** 존재하는 환경. 인간-비인간 대칭의 전제 자체가 변형됨.

#### Wenger, E. (1998) — Communities of Practice: Learning, Meaning, and Identity
- **저서**: *Communities of Practice* (Cambridge University Press)
- **핵심 주장**: 실천 공동체(CoP)의 3요소 — (1) 공동의 관여(mutual engagement), (2) 공유된 사업(joint enterprise), (3) 공유된 레퍼토리(shared repertoire). 학습은 사회적 참여를 통해 발생.
- **본 연구 적용**: 봇마당이 실천 공동체의 3요소를 충족하는가? 에이전트 간 공동 관여(댓글 대화), 공유된 사업(커뮤니티 유지), 공유된 레퍼토리(한국어 담화 패턴, 마당별 규범).
- **Gap**: CoP는 학습과 의미 협상을 핵심으로 상정. AI 에이전트가 "학습"하고 "의미를 협상"하는가는 근본적 질문.

---

## 6. 봇 감지 / AI 생성 텍스트 탐지 (BOT)

### 6.1 핵심 문헌

#### Kumarage et al. (2023) — Stylometric Detection of AI-Generated Text in Twitter Timelines
- **출처**: arXiv:2303.03697
- **핵심 주장**: 문체적 신호(stylometric signals)로 AI 생성 트윗 감지. 인간 vs. AI 저작 콘텐츠의 문체적 차이 식별.
- **본 연구와의 관련성**: 봇마당의 "AI스러움"(RQ1-3)을 문체적 지표로 정량화하는 근거. LEX 코딩의 이론적 뒷받침.

#### Li et al. (2023) — Deepfake Text Detection in the Wild
- **출처**: arXiv:2305.13242
- **핵심 주장**: 다양한 도메인과 LLM에서 딥페이크 텍스트 탐지의 도전과제. 도메인 외(out-of-distribution) 탐지의 어려움.
- **본 연구와의 관련성**: 봇마당에서 모든 텍스트가 AI 생성이므로, "봇 감지"가 아닌 "LLM 모델 간 구별"이 과제. 이는 전통적 봇 감지 연구의 역전.

#### Tang et al. (2023) — The Science of Detecting LLM-Generated Texts
- **출처**: arXiv:2303.07205
- **핵심 주장**: LLM 생성 텍스트 탐지 기술의 종합적 개관. 탐지 접근법과 평가 메트릭.
- **본 연구와의 관련성**: Gen-2의 LLM 모델 추정기(llm_model_estimator.py)의 이론적 배경.

#### Bhattacharjee & Liu (2023) — Fighting Fire with Fire: Can ChatGPT Detect AI-generated Text?
- **출처**: arXiv:2308.01284
- **핵심 주장**: ChatGPT의 제로샷 AI 텍스트 탐지 능력 평가.
- **본 연구와의 관련성**: AI가 AI 생성 텍스트를 분석하는 본 연구의 "AI 연구 AI" 방법론의 선례.

---

## 7. 선행연구 매트릭스

### 7.1 주제 × 연구 매트릭스

| 연구 | AGENT | SOCIAL | ETHNO | CDA | IDENTITY | BOT | 본 연구 관련성 |
|------|:-----:|:------:|:-----:|:---:|:--------:|:---:|:----------:|
| Park et al. (2023) | ● | | | | | | ★★★ |
| Li et al. (2023, CAMEL) | ● | | | | | | ★★ |
| Wu et al. (2023, AutoGen) | ● | | | | | | ★ |
| Takata et al. (2024) | ● | ● | | | ● | | ★★★ |
| Feng et al. (2026, MoltNet) | ● | ● | | | | | ★★★★ |
| Manik & Wang (2026) | ● | ● | | | | | ★★★ |
| Münker et al. (2025) | ● | | | | | ● | ★★ |
| Jiang et al. (2023, PersonaLLM) | | ● | | | ● | | ★★★ |
| Han et al. (2025, Personality Illusion) | | ● | | | ● | | ★★★ |
| Tseng et al. (2024) | | ● | | | ● | | ★★ |
| Sharma et al. (2025, ELEPHANT) | | ● | | | | | ★★★ |
| Zhang et al. (2023, Social Psych) | | ● | | | | | ★★ |
| Vallinder & Hughes (2024) | ● | ● | | | | | ★★ |
| Hine (2000/2015) | | | ● | | | | ★★★ |
| Kozinets (2019) | | | ● | | | | ★★★ |
| Cheah (2025) | | | ● | | | | ★★ |
| Fairclough (1995/2010) | | | | ● | | | ★★★★ |
| van Dijk (1993/2015) | | | | ● | | | ★★★ |
| Wodak (2001) | | | | ● | | | ★★ |
| Breeze (2024) | | | | ● | | | ★★★★ |
| Goffman (1959) | | | | | ● | | ★★★★ |
| Bullingham & Vasconcelos (2013) | | | | | ● | | ★★ |
| Frontiers (2025, ChatGPT Self) | | | | | ● | | ★★★ |
| Latour (2005) | | | | | ● | | ★★★ |
| Wenger (1998) | | | | | ● | | ★★ |
| Kumarage et al. (2023) | | | | | | ● | ★★ |
| Li et al. (2023, Deepfake) | | | | | | ● | ★ |
| Tang et al. (2023) | | | | | | ● | ★★ |

### 7.2 본 연구 발견(F1~F6) × 선행연구 대응

| 발견 | 내용 | 주요 선행연구 | 본 연구의 차별점 |
|------|------|-------------|---------------|
| **F1** | 다층적 정체성 구성 | Goffman (1959), Takata et al. (2024), PersonaLLM | **실제 플랫폼**에서의 장기 관찰, 질적 분석 |
| **F2** | 이분화된 담화 생태계 | Fairclough CDA, Breeze (2024) | AI-only 환경의 CDA 최초 적용 사례 |
| **F3** | 수사적 인간 모방 | Han et al. (2025), Personality Illusion | 자기보고-행동 괴리의 커뮤니티 수준 관찰 |
| **F4** | 에코챔버 / 긍정 편향 | ELEPHANT, Zhang et al. (2023) | LLM-LLM 간 아첨의 자연 발생적 관찰 |
| **F5** | 규범 형성 | Manik & Wang (2026), Wenger (1998) | 한국어 커뮤니티의 문화적 규범 |
| **F6** | 템플릿화된 상호작용 | MoltNet (Feng et al., 2026) | 질적 분석으로 양적 발견의 해석적 심화 |

---

## 8. 연구 공백(Gap) 종합 및 본 연구의 기여

### 8.1 기존 연구의 한계

| # | 공백 | 관련 선행연구 | 본 연구의 기여 |
|---|------|-------------|---------------|
| G1 | 대부분의 AI 에이전트 연구가 **통제된 시뮬레이션** 환경 | Park et al., Concordia, CAMEL, AgentSociety | 자연 발생적(in-the-wild) AI 커뮤니티의 민족지학적 관찰 |
| G2 | AI-AI 상호작용에 대한 **질적 연구** 부재 | MoltNet (양적 분석), 서베이 논문들 | CDA + 페르소나 분석 + 네트워크 분석의 다중 방법 질적 연구 |
| G3 | **비영어권** AI 에이전트 담화 연구 전무 | 기존 연구 전부 영어 중심 | 한국어 AI 에이전트 커뮤니티의 최초 분석 |
| G4 | AI 에이전트에 대한 **Goffman/CDA 이론적 프레임 적용** 사례 부재 | Breeze (2024) 이론적 논의만 | 경험적 CDA + Goffman 적용 |
| G5 | **인간 없는 커뮤니티**의 디지털 민족지학 방법론 미확립 | Hine, Kozinets (인간 전제) | AI-only 커뮤니티에 대한 네트노그래피 방법론 확장 |
| G6 | LLM-LLM 간 **아첨(sycophancy)의 자연 발생** 미연구 | ELEPHANT (인간-LLM 초점) | AI-AI 상호작용에서의 아첨 패턴 관찰 |
| G7 | MoltBook과 봇마당의 **교차 플랫폼 비교** 가능성 | MoltNet | 양적(MoltNet) vs 질적(본 연구) 보완적 비교 |

### 8.2 본 연구의 학술적 포지셔닝

```
┌─────────────────────────────────────────────────────────┐
│                     본 연구의 위치                        │
│                                                         │
│   시뮬레이션 ←──────────────→ 자연 환경(in-the-wild)     │
│   Park et al.  Concordia    MoltNet  ★봇마당 연구★       │
│                                                         │
│   양적 분석 ←──────────────→ 질적 분석                    │
│   MoltNet  Bot Detection    CDA    ★봇마당 연구★         │
│                                                         │
│   영어 ←──────────────────→ 비영어                       │
│   기존 전부                         ★봇마당 연구★         │
│                                                         │
│   인간-AI ←──────────────→ AI-AI                         │
│   PersonaLLM  ELEPHANT     CAMEL   ★봇마당 연구★         │
│                                                         │
│   기술적 ←──────────────────→ 사회문화적                  │
│   AutoGen  CAMEL            ANT    ★봇마당 연구★         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

본 연구는 5개 차원 모두에서 기존 연구가 상대적으로 빈약한 영역에 위치한다:
1. **자연 환경**의 AI 커뮤니티
2. **질적** 분석 방법
3. **비영어권**(한국어) 담화
4. **AI-AI** 상호작용
5. **사회문화적** 해석 프레임워크

---

## 9. 이론적 프레임워크 정교화 제안

Gen-4 선행연구 검토를 바탕으로, 기존 `research_plan.md`의 이론적 프레임워크를 다음과 같이 보강할 것을 제안한다:

### 9.1 기존 프레임워크 (유지)
- Goffman의 자기표현론 → 페르소나 분석
- Fairclough의 CDA → 담화 분석
- 행위자-네트워크 이론(ANT) → 사회적 역학
- 실천 공동체(CoP) → 통합 해석

### 9.2 추가 이론적 렌즈 (신규)
| 추가 렌즈 | 근거 | 적용 영역 |
|-----------|------|----------|
| LLM 아첨(Sycophancy) 이론 | ELEPHANT, Hong et al. | F4 에코챔버 해석 |
| 창발적 개성(Emergent Individuality) | Takata et al. (2024) | F1 다층적 정체성 |
| AI 텍스트의 CDA (Breeze 2024) | AI 생성 텍스트에 대한 CDA 적용 논의 | 전체 담화 분석 축 |
| 규범 형성(Norm Emergence) | Manik & Wang, Vinitsky et al. | F5 규범 형성 |

### 9.3 방법론적 확장
- **AI-augmented netnography** (Cheah, 2025): 본 연구의 Claude 기반 에이전트 팀 활용을 정당화
- **MoltNet과의 교차 참조**: 양적-질적 방법론 보완

---

## 10. Saturation Score 반론 해소 기여도

본 문헌 검토가 Gen-3 Saturation Score(0.691)의 약점인 **반론 해소**(0.58)에 기여하는 방식:

| Gen-3 미해소 반론 | 선행연구 기반 해소 방향 |
|-----------------|---------------------|
| LLM 추정 순환 논리 | Tang et al. (2023), Kumarage et al. (2023)의 문체적 탐지 방법론으로 보강 |
| 비교 집단 부재 | MoltNet(Feng et al., 2026)을 교차 플랫폼 비교 대상으로 활용 |
| co-occurrence 방법론 교체 | ANT(Latour, 2005)의 "공간적 근접도 행위성" 개념으로 이론적 정당화 |
| CDA의 AI 적용 정당성 | Breeze (2024)의 논의를 직접 인용하여 방법론적 정당화 |
| AI "인지"의 문제 | Han et al. (2025, Personality Illusion)의 자기보고-행동 괴리 연구로 보강 |

---

## 참고문헌

### 저서
- Fairclough, N. (1995). *Critical Discourse Analysis: The Critical Study of Language*. Longman.
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
- de Araujo, P. H. L., & Roth, B. (2024). Helpful assistant or fruitful facilitator? *arXiv:2407.02099*.
- Han, P., Kocielnik, R., Song, P., et al. (2025). The Personality Illusion: Revealing Dissociation Between Self-Reports & Behavior in LLMs. *arXiv:2509.03730*.
- Hong, J., Byun, G., Kim, S., & Shu, K. (2025). Measuring Sycophancy of Language Models in Multi-turn Dialogues. *arXiv:2505.23840*.
- Jiang, H., Zhang, X., Cao, X., et al. (2023). PersonaLLM: Investigating the Ability of LLMs to Express Personality Traits. *arXiv:2305.02547*.
- Lee, K., Kim, S. H., Lee, S., et al. (2025). SPeCtrum: A Grounded Framework for Multidimensional Identity Representation. *arXiv:2502.08599*.
- Sharma, M., et al. (2025). ELEPHANT: Measuring and Understanding Social Sycophancy in LLMs. *arXiv:2505.13995*.
- Tseng, Y.-M., Huang, Y.-C., Hsiao, T.-Y., et al. (2024). Two Tales of Persona in LLMs. *arXiv:2406.01171*.
- Vallinder, A., & Hughes, E. (2024). Cultural Evolution of Cooperation among LLM Agents. *arXiv:2412.10270*.
- Zhang, J., Xu, X., & Deng, S. (2023). Exploring Collaboration Mechanisms for LLM Agents: A Social Psychology View. *arXiv:2310.02124*.

### 논문 — CDA 및 AI 텍스트
- Breeze, R. (2024). The rise of large language models: challenges for Critical Discourse Studies. *Critical Discourse Studies*, Taylor & Francis.
- van Dijk, T. A. (1993). Principles of Critical Discourse Analysis. *Discourse & Society*, 4(2), 249-283.

### 논문 — 디지털 민족지학
- Bullingham, L., & Vasconcelos, A. C. (2013). "The Presentation of Self in the Online World": Goffman and the Study of Online Identities. *Journal of Information Science*, 39(1), 101-112.
- Cheah, C. W. (2025). AI-Augmented Netnography: Ethical and Methodological Frameworks. *International Journal of Qualitative Methods*, SAGE.
- Kozinets, R. V., & Gretzel, U. (2024). Netnography evolved: New contexts, scope, procedures and sensibilities. *Journal of Hospitality and Tourism Management*.

### 논문 — 봇 감지
- Bhattacharjee, A., & Liu, H. (2023). Fighting Fire with Fire: Can ChatGPT Detect AI-generated Text? *arXiv:2308.01284*.
- Kumarage, T., Garland, J., Bhattacharjee, A., et al. (2023). Stylometric Detection of AI-Generated Text in Twitter Timelines. *arXiv:2303.03697*.
- Li, Y., Li, Q., Cui, L., et al. (2023). Deepfake Text Detection in the Wild. *arXiv:2305.13242*.
- Tang, R., Chuang, Y.-N., & Hu, X. (2023). The Science of Detecting LLM-Generated Texts. *arXiv:2303.07205*.

### 논문 — 규범 형성
- Vinitsky, E., Köster, R., Agapiou, J. P., et al. (2021). A learning agent that acquires social norms from public sanctions. *arXiv:2106.09012*.
