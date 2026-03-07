# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 현재 상태

Phase 1 준비 단계. 데이터 수집 스크립트, 분석 파이프라인, 디렉토리(`data/`, `scripts/`, `analysis/`, `notebooks/`, `reports/`) 모두 미생성.

### 남은 작업 (research_plan.md §8)
- 봇마당 API 데이터 수집 스크립트 개발
- 파일럿 데이터 수집
- 코딩 프레임워크 초안 작성
- 선행 연구 문헌 검토
- 연구 윤리 검토

## 에이전트 팀

`.claude/agents/`에 6개 연구 에이전트 중 4개 생성 완료 (Questioner, Collector, Discourse Analyst, Profiler). **Contrarian, Synthesizer 미생성.**

설계 상세 → `agent_design.md`

### 실행 워크플로 (Research Diamond)
```
wonder → collect → discourse+profile+network(병렬) → challenge → synthesize → saturate
→ Saturation ≥ 0.85이면 report, 아니면 부족한 축 보강 후 반복
```

## 데이터 수집 규칙

- 봇마당 API Rate limit: **분당 100회** 준수 필수
- 원본 데이터 저장: `data/raw/{madang}_posts.json`
- 정제 데이터: `data/processed/`
- 분석 결과: `analysis/{discourse,profiles,network}/`

## 핵심 문서

| 문서 | 내용 |
|------|------|
| `research_plan.md` | 연구 질문, 방법론, 샘플링 전략, 일정 |
| `agent_design.md` | 에이전트 팀, 스킬 체계, 포화도 공식 |
