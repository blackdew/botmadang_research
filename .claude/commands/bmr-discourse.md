# /bmr discourse — 담화 분석 파이프라인

> Phase 2: 분석 | 담당: Discourse Analyst 에이전트

$ARGUMENTS 파싱:
- `--issue N`: 기존 이슈 #N에 연결
- `--corpus <경로>`: 분석 대상 코퍼스 경로 (기본: data/processed/)
- `--focus <항목>`: 특정 분석 층위에 집중 (lexical, sentence, structure, pragmatic, intertextual)
- 인자 없음: 새 이슈 자동 생성 + 전체 파이프라인 실행

## 실행 흐름

### Phase 0: 이슈 준비

```
gh issue create --title "[Discourse] <분석 대상> 담화 분석" \
  --label "discourse,phase-2:분석" \
  --body "## 상위 이슈\n- Epic: #2\n\n## 목표\n수집된 코퍼스에 대한 다층적 담화 분석\n\n## 담당 에이전트\n- Discourse Analyst (담화 분석가)\n\n## 입력\n- 코퍼스: <경로>\n\n## 기대 산출물\n- analysis/discourse/ 디렉토리에 분석 결과"
```

### Phase 1: Discourse Analyst 에이전트 호출

Discourse Analyst(`.claude/agents/discourse-analyst.md`)를 호출하여 다음 파이프라인 실행:

1. **어휘 분석**: 형태소 분석(KoNLPy/Kiwi), TTR 계산, 고빈도 어휘 추출
2. **문체 분류**: 존댓말/반말 비율, 격식/비격식 분포
3. **담화 구조 코딩**: 도입-전개-결론 패턴, 논증 방식
4. **화용론 분석**: 완화 표현, 감정 표현
5. **"AI스러움" 지표 추출**: 반복 패턴, 과도한 구조화 등
6. **상호텍스트성**: 인용, 참조, 밈 사용

분석 중 주요 발견 시 이슈에 댓글:
```
gh issue comment <이슈번호> --body "## 📊 Discourse Analyst 중간 발견\n[발견 내용]"
```

### Phase 2: 결과 저장 + 이슈 완료

1. 분석 결과를 `analysis/discourse/`에 저장
2. 이슈에 완료 댓글 + 결과 요약
3. 이슈 닫기
