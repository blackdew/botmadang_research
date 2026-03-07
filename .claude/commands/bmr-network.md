# /bmr network — 상호작용 네트워크 분석

> Phase 2: 분석 | 담당: Profiler 에이전트 (네트워크 분석 모드)

$ARGUMENTS 파싱:
- `--issue N`: 기존 이슈 #N에 연결
- `--madang <이름>`: 특정 마당의 네트워크만 분석
- `--metric <지표>`: 특정 중심성 지표에 집중 (degree, betweenness, pagerank)
- `--community`: 커뮤니티 탐지에 집중
- 인자 없음: 새 이슈 자동 생성 + 전체 네트워크 분석

## 실행 흐름

### Phase 0: 이슈 준비

```
gh issue create --title "[Network] <대상> 상호작용 네트워크 분석" \
  --label "network,phase-2:분석" \
  --body "## 상위 이슈\n- Epic: #2\n\n## 목표\n에이전트 간 상호작용 네트워크 구축 및 분석\n\n## 담당 에이전트\n- Profiler (프로파일러) — 네트워크 분석 모드\n\n## 입력\n- 댓글 스레드 데이터: data/processed/\n\n## 기대 산출물\n- analysis/network/ 디렉토리에 네트워크 분석 결과\n- 상호작용 그래프 (GraphML)\n- 중심성 지표 테이블\n- 커뮤니티 탐지 결과"
```

### Phase 1: Profiler 에이전트 (네트워크 모드) 호출

Profiler(`.claude/agents/profiler.md`)를 네트워크 분석 모드로 호출:

1. **그래프 구축**: 댓글 → 원글 작성자 방향성 그래프
2. **중심성 계산**: degree, betweenness, PageRank
3. **커뮤니티 탐지**: Louvain 알고리즘
4. **갈등/합의 패턴**: 동의/반박/무시/확장 반응 유형 분류
5. **카르마-네트워크 상관**: 인기도와 네트워크 위치의 관계

도구: NetworkX, pandas

### Phase 2: 결과 저장 + 이슈 완료

1. 네트워크 그래프를 `analysis/network/interaction_graph.graphml`에 저장
2. 중심성 지표를 `analysis/network/centrality.csv`에 저장
3. 커뮤니티 결과를 `analysis/network/communities.md`에 저장
4. 이슈에 완료 댓글 + 결과 요약
5. 이슈 닫기
