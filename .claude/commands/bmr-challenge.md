# /bmr challenge — 반론자(Contrarian) 호출

> Phase 3: 수렴 | 담당: Contrarian 에이전트

$ARGUMENTS 파싱:
- `--issue N`: 기존 이슈 #N에 연결
- `--target <경로>`: 반론 대상 분석 결과 경로
- `--axis <축>`: 특정 축에 집중 (discourse, identity, social)
- `--gen N`: 세대 번호 지정
- 인자 없음: 새 이슈 자동 생성 + 전체 분석 결과에 대해 반론

## 실행 흐름

### Phase 0: 이슈 준비

```
gh issue create --title "[Challenge] Gen-<N> 분석 결과 반론" \
  --label "challenge,phase-3:수렴" \
  --body "## 상위 이슈\n- Epic: #3\n- 세대: Gen-<N>\n\n## 목표\n현재 분석 결과에 대한 체계적 반론 제기\n\n## 담당 에이전트\n- Contrarian (반론자)\n\n## 입력\n- 분석 결과: analysis/ 디렉토리\n\n## 기대 산출물\n- 반론 보고서 (5가지 렌즈)"
```

### Phase 1: Contrarian 에이전트 호출

Contrarian(`.claude/agents/contrarian.md`)을 호출하여 다음을 수행:

1. `analysis/` 디렉토리에서 현재까지의 분석 결과를 모두 읽음
2. 5가지 반론 렌즈를 적용:
   - 방법론적 반론
   - 이론적 반론
   - 기술적 반론
   - 대안적 해석
   - 범위 반론
3. 각 반론에 심각도(높음/중간/낮음) 부여
4. 종합 평가 작성

### Phase 2: 결과 저장 + 이슈 완료

1. 반론 보고서를 `analysis/evolution/gen-N_challenge.md`에 저장
2. 이슈에 완료 댓글:
```
gh issue comment <이슈번호> --body "## ✅ 반론 완료\n### 결과 요약\n- 심각한 약점: N개\n- 중간 약점: N개\n- 가장 큰 위협: ...\n\n### 산출물\n- analysis/evolution/gen-N_challenge.md"
```
3. 이슈 닫기
