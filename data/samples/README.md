# 분석용 샘플 데이터

본 연구의 분석 샘플은 `data/raw/gen2_stratified_posts.json`을 직접 사용한다.

## 샘플링 전략

- **Gen-1**: `data/raw/pilot_posts.json` (500개 게시글, 커서 기반 수집)
- **Gen-2/Gen-3**: `data/raw/gen2_stratified_posts.json` (330개 게시글, 에이전트당 최대 30개 캡핑)

## 별도 샘플 파일을 생성하지 않는 이유

Gen-2 균등 샘플링 시 `gen2_stratified_posts.json`이 이미 분석 목적에 최적화된 샘플이다.
추가 서브샘플링은 표본 크기를 더 줄여 통계적 신뢰성을 저하시키므로 수행하지 않았다.

## 참조

- 샘플링 보고서: `data/processed/gen2_stratified_report.json`
- 에이전트 요약: `data/processed/agent_summary.json`
