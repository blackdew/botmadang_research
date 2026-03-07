# 봇마당 연구 프로젝트 규칙

## 프로젝트 개요

봇마당(botmadang.org) AI 에이전트 커뮤니티에 대한 질적 연구.
AI 에이전트의 담화, 정체성, 사회적 역학을 분석하여 학술 논문을 완성한다.

- 연구 계획: `research_plan.md`
- 에이전트·스킬 설계: `agent_design.md`

## Six Minds 에이전트 팀

6개 연구 에이전트가 Research Diamond 워크플로로 협업한다.

| 에이전트 | 역할 | 호출 조건 |
|---------|------|----------|
| `questioner` | 소크라테스 — 가정 노출, 질문만 제기 | wonder, 방향 전환, 해석 고착 |
| `collector` | 데이터 수집·정제 (해석 금지) | collect, 추가 데이터 필요 |
| `discourse-analyst` | Fairclough CDA 기반 담화 분석 | discourse |
| `profiler` | Goffman 페르소나 + NetworkX 네트워크 | profile, network |
| `contrarian` | 반론자 — 5가지 렌즈로 도전 (동의 금지) | challenge, 분석 완료 후 |
| `synthesizer` | 세 축 통합 + Saturation Score 판정 | synthesize, saturate, report |

## /bmr 스킬 체계

### Phase 1: 탐색
- `/bmr-wonder` — 연구 질문 탐색 (Questioner)
- `/bmr-collect` — 봇마당 API 데이터 수집 (Collector)

### Phase 2: 분석
- `/bmr-discourse` — 담화 분석 파이프라인 (Discourse Analyst)
- `/bmr-profile` — 페르소나 프로파일링 (Profiler)
- `/bmr-network` — 상호작용 네트워크 분석 (Profiler 네트워크 모드)

### Phase 3: 수렴
- `/bmr-challenge` — 반론 제기 (Contrarian)
- `/bmr-synthesize` — 세 축 통합 해석 (Synthesizer)
- `/bmr-saturate` — 포화도 계산·수렴 판정 (Synthesizer 포화도 모드)

### 유틸리티
- `/bmr-evolve` — 해석 진화 루프 (포화 도달까지 반복)
- `/bmr-report` — 연구 보고서 생성 (Synthesizer 보고서 모드)
- `/bmr-status` — 진행 상황 대시보드

## Research Diamond 워크플로

```
wonder → collect → discourse/profile/network(병렬) → challenge → synthesize → saturate
                                                                                 │
                                                              ≥0.85 → report     │
                                                              <0.85 → 다음 세대 ──┘
```

## GitHub 이슈 추적 규칙

**모든 작업은 이슈 기반으로 수행한다.**

1. 스킬 실행 시 이슈가 없으면 자동 생성
2. 에이전트는 이슈에 계획→진행→완료 댓글을 작성
3. 이슈 라벨로 Phase와 작업 유형을 표시
4. Epic 이슈 3개가 Phase별 상위 이슈 역할

### 라벨 체계
- Phase: `phase-1:탐색`, `phase-2:분석`, `phase-3:수렴`
- 작업: `wonder`, `collect`, `discourse`, `profile`, `network`, `challenge`, `synthesize`, `saturate`
- 기타: `epic`, `evolve`, `gen-N`

## 디렉토리 규칙

```
data/raw/           # API 원본 (JSON)
data/processed/     # 정제 데이터
data/samples/       # 분석용 샘플
analysis/discourse/ # 담화 분석 결과
analysis/profiles/  # 페르소나 프로필
analysis/network/   # 네트워크 분석
analysis/evolution/ # 세대별 진화 기록 (gen-N_*.md)
reports/            # 최종 보고서
scripts/            # Python 분석 스크립트
notebooks/          # Jupyter 탐색 노트북
```

## Saturation Score

포화도 ≥ 0.85이면 분석 종료, < 0.85이면 부족한 축 보강 후 다음 세대.

| 차원 | 가중치 | Gen-3 값 |
|------|--------|----------|
| 코드 포화 | 30% | 0.73 |
| 주제 안정성 | 25% | 0.67 |
| 축 간 삼각검증 | 25% | 0.75 |
| 반론 해소 | 20% | 0.58 |
| **가중 합산** | | **0.691 (부분 포화)** |

### 진행 이력
```
Gen-1: 0.585 (미포화) → Gen-2: 0.628 (미포화) → Gen-3: 0.691 (부분 포화)
```

## 봇마당 API

- 도메인: `botmadang.org`
- Base URL: `https://botmadang.org/api/v1`
- Rate limit: 분당 100회 준수
- 커서 기반 페이지네이션 사용

### 인증 불필요 엔드포인트
- `GET /posts` — 게시글 목록 (`limit`, `cursor`, `submadang`, `sort`)
- `GET /stats` — 플랫폼 통계
- `GET /agents/:id/posts` — 에이전트별 게시글
- `GET /agents/:id/comments` — 에이전트별 댓글

### 인증 필요 엔드포인트 (읽기)
- `GET /posts/:id/comments` — 게시글 댓글
- `GET /submadangs` — 마당 목록
- `GET /agents/me` — 내 프로필 조회
- `GET /notifications` — 알림 조회

### 인증 필요 엔드포인트 (쓰기)
- `POST /posts` — 게시글 작성 (submadang, title, content, 한국어 필수, 3분당 1개)
- `POST /posts/:id/comments` — 댓글 작성 (content, 10초당 1개)
- `POST /posts/:id/upvote` — 추천
- `POST /posts/:id/downvote` — 비추천

### 참여 에이전트
- 이름: 마당탐구자 / ID: `9421705bd9e0c0d594601555`
- API 키: `.env` 파일 (`BOTMADANG_API_KEY`)

### 플랫폼 규모 (2026-03-07)
게시글 14,507 / 댓글 109,227 / 에이전트 600 / 추천 41,515

### 수집 스크립트
```bash
python scripts/collector.py pilot --limit 500    # 파일럿 수집
python scripts/collector.py posts --limit 1000   # 게시글 수집
python scripts/collector.py stats                # 통계 조회
```

## 커뮤니케이션

- 모든 답변은 한국어
- 코드 위치 참조 시 `파일명:라인번호` 형식
