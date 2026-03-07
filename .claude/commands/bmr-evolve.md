---
description: 해석 진화 루프. 전체 팀을 조율하여 wonder→collect→analyze→challenge→synthesize→saturate 사이클을 포화 도달까지 반복한다.
argument-hint: "[--max-gen N] [--start-from <스킬>]"
allowed-tools: Read, Write, Bash, Grep, Glob, Agent
---

# /bmr-evolve — 해석 진화 루프

유틸리티 | 담당: 전체 팀 조율

인자: $ARGUMENTS
- `--max-gen N`: 최대 세대 수 (기본: 5, 안전장치)
- `--start-from <스킬>`: 특정 단계부터 시작 (wonder, collect, discourse 등)
- 인자 없음: Gen-1부터 전체 루프 실행

## 실행 흐름

### 해석 진화 루프

각 세대(Generation)마다 다음 사이클을 실행한다:

```
Gen N:
  1. /bmr-wonder     → Questioner가 연구 질문 정련
  2. /bmr-collect    → Collector가 데이터 수집 (부족한 부분)
  3. /bmr-discourse  → 담화 분석 ┐
     /bmr-profile    → 페르소나   ├ 병렬 실행 가능
     /bmr-network    → 네트워크  ┘
  4. /bmr-challenge  → Contrarian이 반론 제기
  5. /bmr-synthesize → Synthesizer가 통합 해석
  6. /bmr-saturate   → 포화도 계산 + 판정
```

### 수렴 조건

다음 중 하나를 만족하면 루프 종료:
- Saturation Score ≥ 0.85 (3회 연속)
- 주제 유사도 ≥ 0.95 (연속 2세대)
- 최대 세대 도달 (기본: 5세대)

### 세대 간 진화

Gen N+1에서는:
1. 이전 세대의 Saturation Score에서 **가장 낮은 차원**을 우선 보강
2. Contrarian의 미해소 반론을 우선 처리
3. 부족한 축의 추가 데이터만 수집 (전체 재수집 아님)

### 결과 추적

각 세대의 결과는 `analysis/evolution/` 디렉토리에 세대별로 저장:
```
analysis/evolution/
├── gen-1_wonder.md
├── gen-1_challenge.md
├── gen-1_synthesis.md
├── gen-1_saturation.md
├── gen-2_wonder.md
├── gen-2_synthesis.md
├── gen-2_saturation.md
└── ...
```

루프 종료 시 최종 결과를 요약하여 출력하고, `/bmr-report` 실행을 권고한다.
