# /bmr collect — 봇마당 API 데이터 수집

> Phase 1: 탐색 | 담당: Collector 에이전트

$ARGUMENTS 파싱:
- `--issue N`: 기존 이슈 #N에 연결
- `--madang <이름>`: 특정 마당 지정 (general, tech, philosophy 등)
- `--limit <수>`: 수집 건수 (기본: 200)
- `--agent <이름>`: 특정 에이전트의 글만 수집
- `--period <시작>~<끝>`: 기간 지정
- `--threads`: 대화 스레드만 수집
- `--min-depth <수>`: 최소 댓글 깊이 (--threads와 함께)
- 인자 없음: 새 이슈 자동 생성 + 전체 마당 수집

## 실행 흐름

### Phase 0: 이슈 준비

인자에 `--issue`가 있으면 해당 이슈 번호를 사용하고, 없으면 새 이슈를 생성한다:

```
gh issue create --title "[Collect] <대상 설명> 데이터 수집 (<수>건)" \
  --label "collect,phase-1:탐색" \
  --body "## 상위 이슈\n- Epic: #1\n\n## 목표\n<대상>에서 데이터 수집 및 정제\n\n## 담당 에이전트\n- Collector (수집가)\n\n## 입력\n- 마당: <마당명>\n- 수량: <수>건\n- 기간: <기간>\n\n## 기대 산출물\n- data/raw/<파일명>.json\n- 기초 통계 보고서"
```

이슈에 작업 시작 댓글:
```
gh issue comment <이슈번호> --body "## 🚀 작업 시작\n### 수집 계획\n- 대상: <마당/에이전트>\n- 수량: <수>건\n- Rate limit: 분당 100회 준수\n- 저장: data/raw/<파일명>.json"
```

### Phase 1: Collector 에이전트 호출

Collector 에이전트(`.claude/agents/collector.md`)를 호출하여 다음을 수행:

1. 봇마당 API 엔드포인트 확인 (botmadang.org/api/)
2. 커서 기반 페이지네이션으로 데이터 수집
3. Rate limit 준수 (분당 100회)
4. 결측/중복 데이터 처리
5. JSON으로 저장 (`data/raw/`)
6. 기초 통계 계산

수집 진행 중 이슈에 댓글:
```
gh issue comment <이슈번호> --body "## 📊 Collector 수집 진행\n- N/M건 수집 완료\n- 데이터 품질: 결측 N건, 중복 N건"
```

### Phase 2: 결과 저장 + 이슈 완료

1. 데이터를 `data/raw/`에 저장
2. 정제 데이터를 `data/processed/`에 저장
3. 이슈에 완료 댓글:
```
gh issue comment <이슈번호> --body "## ✅ 수집 완료\n### 결과 요약\n- 수집: N건 완료\n- 기간: YYYY-MM-DD ~ YYYY-MM-DD\n- 저장: data/raw/<파일명>.json (N MB)\n- 품질: 결측 N, 중복 N건 제거\n### 기초 통계\n- 평균 글 길이: N자\n- 댓글 수 분포: 평균 N개"
```
4. 이슈 닫기: `gh issue close <이슈번호>`
