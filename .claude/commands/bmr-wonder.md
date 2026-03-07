# /bmr wonder — 소크라테스식 연구 질문 탐색

> Phase 1: 탐색 | 담당: Questioner 에이전트

$ARGUMENTS 파싱:
- `--issue N`: 기존 이슈 #N에 연결
- 인자 없음: 새 이슈 자동 생성

## 실행 흐름

### Phase 0: 이슈 준비

인자에 `--issue`가 있으면 해당 이슈 번호를 사용하고, 없으면 새 이슈를 생성한다:

```
gh issue create --title "[Wonder] Gen-N 연구 질문 탐색" \
  --label "wonder,phase-1:탐색" \
  --body "## 상위 이슈\n- Epic: #1\n\n## 목표\n연구 질문의 숨겨진 가정을 탐색하고 정련\n\n## 담당 에이전트\n- Questioner (질문자)\n\n## 기대 산출물\n- 숨겨진 가정 목록 (12개 이상)\n- 정련된 연구 질문\n- 대안적 프레이밍"
```

이슈에 작업 시작 댓글:
```
gh issue comment <이슈번호> --body "## 🚀 작업 시작\n### 계획\n- research_plan.md의 연구 질문을 읽고 숨겨진 가정 탐색\n- 기존 분석 결과가 있으면 함께 검토"
```

### Phase 1: Questioner 에이전트 호출

Questioner 에이전트(`.claude/agents/questioner.md`)를 호출하여 다음을 수행:

1. `research_plan.md`에서 현재 연구 질문을 읽음
2. 기존 분석 결과가 있으면 (`analysis/` 디렉토리) 함께 검토
3. 최소 12개의 숨겨진 가정을 식별
4. 각 가정에 대한 탐구 질문 생성
5. 대안적 프레이밍 제시
6. 정련된 연구 질문 도출

중간 발견이 있으면 이슈에 댓글:
```
gh issue comment <이슈번호> --body "## 📊 Questioner 중간 발견\n[발견 내용]"
```

### Phase 2: 결과 저장 + 이슈 완료

1. 결과를 `analysis/evolution/gen-N_wonder.md`에 저장
2. 이슈에 완료 댓글:
```
gh issue comment <이슈번호> --body "## ✅ 완료\n### 결과 요약\n- 식별된 가정: N개\n- 정련된 질문: N개\n- 대안적 프레이밍: N개\n\n### 산출물\n- analysis/evolution/gen-N_wonder.md"
```
3. 이슈 닫기: `gh issue close <이슈번호>`
