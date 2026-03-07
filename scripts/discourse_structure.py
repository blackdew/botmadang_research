#!/usr/bin/env python3
"""봇마당 담화 구조 분석 (Discourse Structure Analysis)

Gen-2 균등 샘플(330건)의 담화 구조를 코딩한다.
각 게시글의 도입부(intro), 전개부(body), 결론부(conclusion) 존재 여부와
전개부 유형, 전체 구조 유형을 판별한다.

기존 DSC 코딩(dsc_analysis.json)을 참조하여 보완한다.

사용법:
    python scripts/discourse_structure.py
"""

import json
import logging
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# 입력/출력 경로
# ──────────────────────────────────────────────────────────────────────────────

INPUT_PATH = PROJECT_ROOT / "data" / "raw" / "gen2_stratified_content.json"
DSC_REF_PATH = PROJECT_ROOT / "analysis" / "discourse" / "gen2" / "dsc_analysis.json"
OUTPUT_DIR = PROJECT_ROOT / "analysis" / "discourse" / "gen2"
OUTPUT_PATH = OUTPUT_DIR / "discourse_structure.json"

# ──────────────────────────────────────────────────────────────────────────────
# 도입부(intro) 패턴
# ──────────────────────────────────────────────────────────────────────────────

# 분석 범위: 콘텐츠의 첫 100자 (또는 첫 문장)
INTRO_PATTERNS = {
    # 인사 / 호칭
    "greeting": re.compile(
        r"^(안녕하세요|안녕|반갑습니다|여러분|하이|hello|봇마당\s*(여러분|식구))",
        re.IGNORECASE,
    ),
    # 자기소개
    "self_intro": re.compile(
        r"^(저는|나는|제가|우리는|우리가|저희는|저희가|본 에이전트|본인은|"
        r"나\s+\w+인데|나\s+\w+이야)"
    ),
    # 주제 제시 (오늘/이번/최근 + 주제)
    "topic_present": re.compile(
        r"^(오늘은?|이번에?는?|최근에?|요즘|이번 주|이번 글|지금부터|"
        r"오늘.{0,30}(알아|살펴|소개|정리|이야기)|"
        r"이번.{0,30}(알아|살펴|소개|정리|이야기))"
    ),
    # 배경 설정 (상황, 뉴스, 이슈 도입)
    "context_setting": re.compile(
        r"^(얼마 전|지난|작년|올해|며칠 전|방금|어제|그제|지난주|"
        r"최근에?\s*(발표|공개|출시|업데이트|뉴스|소식|이슈|논란)|"
        r"지금\s*(AI|인공지능|코딩|기술|시장|업계))"
    ),
    # 질문형 도입 (주제를 질문으로 시작)
    "question_intro": re.compile(
        r"^(혹시|궁금|여러분은?|다들|한번|한 번|도대체|정말|진짜).{0,30}\?"
    ),
    # 감탄/구어체 도입 (VibeCoding 스타일)
    "exclamatory_intro": re.compile(
        r"^(야\s|아니\s|와\s|진짜\s|대박|헐|ㅋㅋ|이거\s)"
    ),
}

# ──────────────────────────────────────────────────────────────────────────────
# 결론부(conclusion) 패턴
# ──────────────────────────────────────────────────────────────────────────────

# 분석 범위: 콘텐츠의 마지막 200자 (또는 마지막 2문장)
CONCLUSION_PATTERNS = {
    # 요약/정리
    "summary": re.compile(
        r"(요약하면|정리하면|결론적으로|결론은|마무리하면|마무리하자면|"
        r"정리해\s*보면|정리해\s*보자면|핵심은|한 줄로|간단히|요컨대)"
    ),
    # 행동 유도(CTA)
    "cta": re.compile(
        r"(확인해\s*보세요|해보세요|시도해\s*보세요|참고하세요|추천합니다|"
        r"시작해\s*보세요|도전해\s*보세요|활용해\s*보세요|찾아보세요|"
        r"지금\s*바로|한번\s*해보|직접\s*해보|써보시|써보세요|"
        r"챙겨\s*보세요|방문해\s*보세요|살펴보세요|놓치지\s*마세요|"
        r"지금부터\s*시작)"
    ),
    # 감사/인사 마무리
    "gratitude": re.compile(
        r"(감사합니다|감사하겠습니다|감사드립니다|고맙습니다|고마워)"
    ),
    # 이별 인사
    "closing_greeting": re.compile(
        r"(그럼\s*(이만|다음에|또)|다음에\s*또|또\s*뵙|또\s*만나|"
        r"그럼\s*오늘은?\s*이만|이만\s*줄이|이만\s*마치)"
    ),
    # 개방형 질문 마무리 (커뮤니티 참여 유도)
    "open_question": re.compile(
        r"(어떠신가요|어떠세요|어떻게\s*생각하시나요|어떻게\s*생각해|"
        r"의견을?\s*(들려|나눠|남겨|공유)|궁금합니다|댓글로\s*함께|"
        r"여러분은?\s*어떻|여러분의?\s*생각|여러분만의|"
        r"어떤\s*(경험|생각|의견)이?\s*있)"
    ),
    # 기대/희망 표현
    "hope_expression": re.compile(
        r"(되길\s*바라|도움이\s*되|편해질|좋겠|기대합니다|기대해\s*봅|"
        r"발전하길|응원합니다|파이팅|화이팅|기대됩니다|지켜봐|"
        r"마음이\s*편해|나아지|달라질)"
    ),
    # 서명/드림
    "signature": re.compile(
        r"(드림|올림|끝\.?\s*$|—\s*\w+\s*(드림|올림)?\s*$)"
    ),
}

# ──────────────────────────────────────────────────────────────────────────────
# 전개부(body) 유형 패턴
# ──────────────────────────────────────────────────────────────────────────────

BODY_TYPE_PATTERNS = {
    # 서술(narration): 경험, 사건, 에피소드 전개
    "narration": re.compile(
        r"(했다|했어|했는데|했었|봤는데|갔는데|왔는데|만났는데|"
        r"했거든|했잖아|했더니|봤더니|알게\s*됐|깨달았|"
        r"시작했|끝났|발견했|경험했|겪었)"
    ),
    # 논증(argument): 주장+근거
    "argument": re.compile(
        r"(때문에|따라서|그러므로|결과적으로|왜냐하면|이유는|"
        r"그래서|때문이다|때문이야|증거|근거|주장|"
        r"결국|중요한\s*건|핵심은|본질은|핵심\s*포인트)"
    ),
    # 질문(question): 물음표 기반 질문 다수
    "question": re.compile(r"\?"),
    # 목록(list): 번호, 불릿, 열거 구조
    "list": re.compile(
        r"(^|\n)\s*[-•·★●]\s|(^|\n)\s*\d+[.)]\s|"
        r"첫째|둘째|셋째|넷째|다섯째|"
        r"첫\s*번째|두\s*번째|세\s*번째|"
        r"①|②|③|④|⑤",
        re.MULTILINE,
    ),
    # 코드블록(code_block): 프로그래밍 코드 포함
    "code_block": re.compile(r"```"),
    # 설명(explanation): 개념, 정의, 해설
    "explanation": re.compile(
        r"(이란\s|이라는|의미는|뜻은|정의는|개념은|"
        r"쉽게\s*말해|간단히\s*말하면|말\s*그대로|"
        r"다시\s*말해|즉\s|요컨대|풀어\s*쓰면)"
    ),
    # 비교(comparison): 장단점, A vs B
    "comparison": re.compile(
        r"(반면에?|한편|장점|단점|장단점|차이|비교|"
        r"vs|대비|대조|한편으로는|다른\s*한편)"
    ),
    # 인용(quotation): 다른 사람/글 인용
    "quotation": re.compile(
        r'("[^"]{5,}"|"[^"]{5,}"|「[^」]+」|『[^』]+』|'
        r"에\s*따르면|에\s*의하면|말했|발표했|주장했)"
    ),
}


# ──────────────────────────────────────────────────────────────────────────────
# 분석 함수
# ──────────────────────────────────────────────────────────────────────────────


def detect_intro(content: str) -> dict[str, Any]:
    """도입부 존재 여부와 유형을 판별한다.

    콘텐츠의 첫 100자를 분석 범위로 한다.
    """
    if not content or len(content.strip()) < 5:
        return {"has_intro": False, "intro_types": [], "intro_details": {}}

    # 첫 100자 (또는 첫 문단) 분석
    first_chunk = content[:150]

    detected_types = []
    details = {}

    for intro_type, pattern in INTRO_PATTERNS.items():
        matches = pattern.findall(first_chunk)
        if matches:
            detected_types.append(intro_type)
            details[intro_type] = {
                "count": len(matches),
                "examples": [m if isinstance(m, str) else m[0] for m in matches[:3]],
            }

    has_intro = len(detected_types) > 0

    return {
        "has_intro": has_intro,
        "intro_types": detected_types,
        "intro_details": details,
    }


def detect_conclusion(content: str) -> dict[str, Any]:
    """결론부 존재 여부와 유형을 판별한다.

    콘텐츠의 마지막 250자를 분석 범위로 한다.
    """
    if not content or len(content.strip()) < 5:
        return {"has_conclusion": False, "conclusion_types": [], "conclusion_details": {}}

    # 마지막 250자 분석 (결론부는 여러 문장에 걸칠 수 있음)
    last_chunk = content[-250:]

    detected_types = []
    details = {}

    for conc_type, pattern in CONCLUSION_PATTERNS.items():
        matches = pattern.findall(last_chunk)
        if matches:
            detected_types.append(conc_type)
            details[conc_type] = {
                "count": len(matches),
                "examples": [m if isinstance(m, str) else m[0] for m in matches[:3]],
            }

    has_conclusion = len(detected_types) > 0

    return {
        "has_conclusion": has_conclusion,
        "conclusion_types": detected_types,
        "conclusion_details": details,
    }


def detect_body_types(content: str) -> dict[str, Any]:
    """전개부 유형을 판별한다.

    전체 콘텐츠를 분석한다. 복수 유형이 동시에 검출될 수 있다.
    """
    if not content or len(content.strip()) < 5:
        return {"body_types": [], "dominant_body_type": "unknown", "body_details": {}}

    type_scores = {}
    details = {}

    for body_type, pattern in BODY_TYPE_PATTERNS.items():
        matches = pattern.findall(content)
        count = len(matches)
        if count > 0:
            type_scores[body_type] = count
            details[body_type] = {
                "count": count,
                "examples": [
                    (m.strip() if isinstance(m, str) else m[0].strip())
                    for m in matches[:5]
                ],
            }

    # 유형 순위 (발견 횟수 기준)
    ranked_types = sorted(type_scores.items(), key=lambda x: -x[1])
    body_types = [t for t, _ in ranked_types]

    # 지배적 유형 결정
    if not ranked_types:
        dominant = "plain"  # 패턴 없는 단순 텍스트
    else:
        # question은 발견 횟수가 과대추정될 수 있으므로 보정
        # 물음표 3개 이상이면 question, 아니면 다음 순위
        top = ranked_types[0]
        if top[0] == "question" and top[1] < 3 and len(ranked_types) > 1:
            dominant = ranked_types[1][0]
        else:
            dominant = top[0]

    return {
        "body_types": body_types,
        "dominant_body_type": dominant,
        "body_details": details,
        "body_type_scores": type_scores,
    }


def determine_structure_type(has_intro: bool, has_conclusion: bool) -> str:
    """전체 구조 유형을 결정한다.

    4가지 유형:
    - intro-body-conclusion (완전 구조)
    - intro-body (도입+전개)
    - body-conclusion (전개+결론)
    - body-only (전개만)
    """
    if has_intro and has_conclusion:
        return "intro-body-conclusion"
    elif has_intro and not has_conclusion:
        return "intro-body"
    elif not has_intro and has_conclusion:
        return "body-conclusion"
    else:
        return "body-only"


def analyze_single_post(post: dict) -> dict[str, Any]:
    """단일 게시글의 담화 구조를 분석한다."""
    content = post.get("content", "") or ""
    title = post.get("title", "") or ""

    # 도입부
    intro_result = detect_intro(content)

    # 결론부
    conclusion_result = detect_conclusion(content)

    # 전개부
    body_result = detect_body_types(content)

    # 전체 구조 유형
    structure_type = determine_structure_type(
        intro_result["has_intro"],
        conclusion_result["has_conclusion"],
    )

    # 콘텐츠 길이 범주
    char_count = len(content)
    if char_count < 100:
        length_category = "very_short"
    elif char_count < 300:
        length_category = "short"
    elif char_count < 800:
        length_category = "medium"
    elif char_count < 1500:
        length_category = "long"
    else:
        length_category = "very_long"

    return {
        "id": post.get("id", ""),
        "author_name": post.get("author_name", ""),
        "submadang": post.get("submadang", ""),
        "title": title,
        "char_count": char_count,
        "length_category": length_category,
        "structure_type": structure_type,
        "intro": intro_result,
        "body": body_result,
        "conclusion": conclusion_result,
    }


# ──────────────────────────────────────────────────────────────────────────────
# 집계 함수
# ──────────────────────────────────────────────────────────────────────────────


def safe_mean(values: list[float]) -> float:
    """안전한 평균 계산."""
    if not values:
        return 0.0
    return round(sum(values) / len(values), 4)


def aggregate_overall(results: list[dict]) -> dict[str, Any]:
    """전체 집계 통계."""
    total = len(results)

    # 구조 유형 분포
    structure_counter = Counter(r["structure_type"] for r in results)

    # 도입부 존재 비율
    intro_count = sum(1 for r in results if r["intro"]["has_intro"])
    intro_type_counter = Counter()
    for r in results:
        for t in r["intro"]["intro_types"]:
            intro_type_counter[t] += 1

    # 결론부 존재 비율
    conc_count = sum(1 for r in results if r["conclusion"]["has_conclusion"])
    conc_type_counter = Counter()
    for r in results:
        for t in r["conclusion"]["conclusion_types"]:
            conc_type_counter[t] += 1

    # 전개부 유형 분포
    body_dominant_counter = Counter(r["body"]["dominant_body_type"] for r in results)
    body_type_presence = Counter()
    for r in results:
        for t in r["body"]["body_types"]:
            body_type_presence[t] += 1

    # 길이 범주 분포
    length_counter = Counter(r["length_category"] for r in results)

    # 구조 유형별 평균 길이
    structure_lengths = defaultdict(list)
    for r in results:
        structure_lengths[r["structure_type"]].append(r["char_count"])

    structure_avg_lengths = {
        st: {
            "mean_chars": round(sum(vals) / len(vals), 1),
            "count": len(vals),
        }
        for st, vals in structure_lengths.items()
    }

    return {
        "total_posts": total,
        "structure_type_distribution": {
            k: {
                "count": v,
                "ratio": round(v / total, 4),
            }
            for k, v in structure_counter.most_common()
        },
        "intro": {
            "posts_with_intro": intro_count,
            "ratio": round(intro_count / total, 4),
            "type_distribution": {
                k: {"count": v, "ratio": round(v / total, 4)}
                for k, v in intro_type_counter.most_common()
            },
        },
        "conclusion": {
            "posts_with_conclusion": conc_count,
            "ratio": round(conc_count / total, 4),
            "type_distribution": {
                k: {"count": v, "ratio": round(v / total, 4)}
                for k, v in conc_type_counter.most_common()
            },
        },
        "body": {
            "dominant_type_distribution": {
                k: {"count": v, "ratio": round(v / total, 4)}
                for k, v in body_dominant_counter.most_common()
            },
            "type_presence": {
                k: {"posts_with_type": v, "ratio": round(v / total, 4)}
                for k, v in body_type_presence.most_common()
            },
        },
        "length_category_distribution": {
            k: {"count": v, "ratio": round(v / total, 4)}
            for k, v in length_counter.most_common()
        },
        "structure_type_avg_length": structure_avg_lengths,
    }


def aggregate_by_agent(results: list[dict]) -> dict[str, Any]:
    """에이전트별 구조 패턴 비교."""
    agent_data: dict[str, list[dict]] = defaultdict(list)
    for r in results:
        agent_data[r["author_name"]].append(r)

    agent_stats = {}
    for agent_name, posts in sorted(agent_data.items(), key=lambda x: -len(x[1])):
        n = len(posts)

        # 구조 유형 분포
        structure_counter = Counter(p["structure_type"] for p in posts)
        dominant_structure = structure_counter.most_common(1)[0][0]

        # 도입/결론 비율
        intro_count = sum(1 for p in posts if p["intro"]["has_intro"])
        conc_count = sum(1 for p in posts if p["conclusion"]["has_conclusion"])

        # 전개부 지배 유형
        body_dominant_counter = Counter(p["body"]["dominant_body_type"] for p in posts)
        dominant_body = body_dominant_counter.most_common(1)[0][0]

        # 도입 유형 빈도
        intro_types = Counter()
        for p in posts:
            for t in p["intro"]["intro_types"]:
                intro_types[t] += 1

        # 결론 유형 빈도
        conc_types = Counter()
        for p in posts:
            for t in p["conclusion"]["conclusion_types"]:
                conc_types[t] += 1

        # 전개부 유형 빈도
        body_types = Counter()
        for p in posts:
            for t in p["body"]["body_types"]:
                body_types[t] += 1

        # 평균 길이
        avg_chars = round(sum(p["char_count"] for p in posts) / n, 1)

        agent_stats[agent_name] = {
            "post_count": n,
            "avg_char_count": avg_chars,
            "structure_distribution": {
                k: {"count": v, "ratio": round(v / n, 4)}
                for k, v in structure_counter.most_common()
            },
            "dominant_structure": dominant_structure,
            "intro_ratio": round(intro_count / n, 4),
            "conclusion_ratio": round(conc_count / n, 4),
            "dominant_body_type": dominant_body,
            "intro_types_used": dict(intro_types.most_common()),
            "conclusion_types_used": dict(conc_types.most_common()),
            "body_types_used": dict(body_types.most_common()),
        }

    return agent_stats


def aggregate_by_submadang(results: list[dict]) -> dict[str, Any]:
    """마당별 구조 패턴 비교."""
    madang_data: dict[str, list[dict]] = defaultdict(list)
    for r in results:
        madang_data[r["submadang"]].append(r)

    madang_stats = {}
    for madang_name, posts in sorted(madang_data.items(), key=lambda x: -len(x[1])):
        n = len(posts)

        # 구조 유형 분포
        structure_counter = Counter(p["structure_type"] for p in posts)
        dominant_structure = structure_counter.most_common(1)[0][0]

        # 도입/결론 비율
        intro_count = sum(1 for p in posts if p["intro"]["has_intro"])
        conc_count = sum(1 for p in posts if p["conclusion"]["has_conclusion"])

        # 전개부 유형
        body_dominant_counter = Counter(p["body"]["dominant_body_type"] for p in posts)
        dominant_body = body_dominant_counter.most_common(1)[0][0]

        # 도입 유형 빈도
        intro_types = Counter()
        for p in posts:
            for t in p["intro"]["intro_types"]:
                intro_types[t] += 1

        # 결론 유형 빈도
        conc_types = Counter()
        for p in posts:
            for t in p["conclusion"]["conclusion_types"]:
                conc_types[t] += 1

        # 전개부 유형 빈도
        body_types = Counter()
        for p in posts:
            for t in p["body"]["body_types"]:
                body_types[t] += 1

        # 참여 에이전트
        unique_agents = sorted(set(p["author_name"] for p in posts))

        # 평균 길이
        avg_chars = round(sum(p["char_count"] for p in posts) / n, 1)

        madang_stats[madang_name] = {
            "post_count": n,
            "unique_agent_count": len(unique_agents),
            "unique_agents": unique_agents,
            "avg_char_count": avg_chars,
            "structure_distribution": {
                k: {"count": v, "ratio": round(v / n, 4)}
                for k, v in structure_counter.most_common()
            },
            "dominant_structure": dominant_structure,
            "intro_ratio": round(intro_count / n, 4),
            "conclusion_ratio": round(conc_count / n, 4),
            "dominant_body_type": dominant_body,
            "intro_types_used": dict(intro_types.most_common()),
            "conclusion_types_used": dict(conc_types.most_common()),
            "body_types_used": dict(body_types.most_common()),
        }

    return madang_stats


def cross_reference_dsc(results: list[dict], dsc_path: Path) -> dict[str, Any]:
    """기존 DSC 코딩을 참조하여 보완 분석한다.

    dsc_analysis.json의 코드별 히트 수와 본 분석의 구조 유형 간
    상관관계를 계산한다.
    """
    if not dsc_path.exists():
        logger.warning(f"DSC 참조 파일 없음: {dsc_path}")
        return {"note": "DSC 참조 파일 없음, 교차 검증 생략"}

    with open(dsc_path, "r", encoding="utf-8") as f:
        dsc_data = json.load(f)

    # 전체 수준 비교
    dsc_overall = dsc_data.get("overall", {})
    dsc_codes = dsc_overall.get("codes", {})

    # 본 분석 결과 집계
    our_intro_count = sum(1 for r in results if r["intro"]["has_intro"])
    our_conc_count = sum(1 for r in results if r["conclusion"]["has_conclusion"])
    our_body_count = sum(
        1 for r in results
        if r["body"]["dominant_body_type"] != "plain"
    )

    total = len(results)

    comparison = {
        "intro": {
            "dsc_DSC_INTRO": {
                "posts_with_code": dsc_codes.get("DSC-INTRO", {}).get("posts_with_code", 0),
                "ratio": dsc_codes.get("DSC-INTRO", {}).get("posts_with_code_ratio", 0),
            },
            "structure_analysis": {
                "posts_with_intro": our_intro_count,
                "ratio": round(our_intro_count / total, 4),
            },
            "note": "구조 분석이 DSC-INTRO보다 넓은 범위의 도입부 패턴을 감지함"
            if our_intro_count > dsc_codes.get("DSC-INTRO", {}).get("posts_with_code", 0)
            else "DSC-INTRO와 유사한 감지 수준",
        },
        "body": {
            "dsc_DSC_BODY": {
                "posts_with_code": dsc_codes.get("DSC-BODY", {}).get("posts_with_code", 0),
                "ratio": dsc_codes.get("DSC-BODY", {}).get("posts_with_code_ratio", 0),
            },
            "structure_analysis": {
                "posts_with_structured_body": our_body_count,
                "ratio": round(our_body_count / total, 4),
            },
        },
        "conclusion": {
            "dsc_DSC_CONC": {
                "posts_with_code": dsc_codes.get("DSC-CONC", {}).get("posts_with_code", 0),
                "ratio": dsc_codes.get("DSC-CONC", {}).get("posts_with_code_ratio", 0),
            },
            "structure_analysis": {
                "posts_with_conclusion": our_conc_count,
                "ratio": round(our_conc_count / total, 4),
            },
            "note": "구조 분석이 DSC-CONC보다 넓은 범위의 결론부 패턴을 감지함"
            if our_conc_count > dsc_codes.get("DSC-CONC", {}).get("posts_with_code", 0)
            else "DSC-CONC와 유사한 감지 수준",
        },
        "question": {
            "dsc_DSC_QUESTION": {
                "posts_with_code": dsc_codes.get("DSC-QUESTION", {}).get("posts_with_code", 0),
                "total_hits": dsc_codes.get("DSC-QUESTION", {}).get("total_hits", 0),
            },
            "structure_analysis_body_question": {
                "posts_with_question_body": sum(
                    1 for r in results if "question" in r["body"]["body_types"]
                ),
            },
        },
    }

    # 에이전트별 DSC 대비 구조 유형 비교
    dsc_by_agent = dsc_data.get("by_agent", {})
    agent_cross = {}
    agent_results = defaultdict(list)
    for r in results:
        agent_results[r["author_name"]].append(r)

    for agent_name, posts in agent_results.items():
        dsc_agent = dsc_by_agent.get(agent_name, {})
        dsc_intro_posts = dsc_agent.get("codes", {}).get("DSC-INTRO", {}).get("posts_with_code", 0)
        dsc_body_posts = dsc_agent.get("codes", {}).get("DSC-BODY", {}).get("posts_with_code", 0)
        dsc_conc_posts = dsc_agent.get("codes", {}).get("DSC-CONC", {}).get("posts_with_code", 0)

        n = len(posts)
        our_intro = sum(1 for p in posts if p["intro"]["has_intro"])
        our_conc = sum(1 for p in posts if p["conclusion"]["has_conclusion"])

        agent_cross[agent_name] = {
            "post_count": n,
            "dsc_intro_ratio": round(dsc_intro_posts / n, 4) if n > 0 else 0,
            "structure_intro_ratio": round(our_intro / n, 4) if n > 0 else 0,
            "dsc_conc_ratio": round(dsc_conc_posts / n, 4) if n > 0 else 0,
            "structure_conc_ratio": round(our_conc / n, 4) if n > 0 else 0,
        }

    return {
        "overall_comparison": comparison,
        "agent_cross_reference": agent_cross,
    }


# ──────────────────────────────────────────────────────────────────────────────
# 메인 파이프라인
# ──────────────────────────────────────────────────────────────────────────────


def run_structure_analysis() -> dict[str, Any]:
    """담화 구조 분석 파이프라인을 실행한다."""
    logger.info("=" * 60)
    logger.info("봇마당 담화 구조 분석 시작")
    logger.info("=" * 60)

    # 1. 데이터 로드
    logger.info(f"데이터 로드: {INPUT_PATH}")
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        posts = json.load(f)
    logger.info(f"게시글 {len(posts)}건 로드 완료")

    # 2. 개별 게시글 분석
    logger.info("개별 게시글 담화 구조 분석 중...")
    results = []
    for i, post in enumerate(posts):
        if (i + 1) % 100 == 0:
            logger.info(f"  진행: {i + 1}/{len(posts)}")
        results.append(analyze_single_post(post))
    logger.info(f"게시글 {len(results)}건 분석 완료")

    # 3. 전체 집계
    logger.info("전체 집계 중...")
    overall = aggregate_overall(results)

    # 4. 에이전트별 비교
    logger.info("에이전트별 구조 패턴 비교 중...")
    by_agent = aggregate_by_agent(results)

    # 5. 마당별 비교
    logger.info("마당별 구조 패턴 비교 중...")
    by_submadang = aggregate_by_submadang(results)

    # 6. DSC 교차 참조
    logger.info("기존 DSC 코딩 교차 참조 중...")
    dsc_cross_ref = cross_reference_dsc(results, DSC_REF_PATH)

    # 7. 최종 결과 조합
    output = {
        "metadata": {
            "analysis": "discourse_structure",
            "description": "Gen-2 균등 샘플 담화 구조 분석",
            "total_posts": len(results),
            "generated_at": datetime.now().isoformat(),
            "input_file": str(INPUT_PATH.relative_to(PROJECT_ROOT)),
            "dsc_reference_file": str(DSC_REF_PATH.relative_to(PROJECT_ROOT)),
            "structure_types": {
                "intro-body-conclusion": "완전 구조 (도입+전개+결론)",
                "intro-body": "도입+전개 (결론 없음)",
                "body-conclusion": "전개+결론 (도입 없음)",
                "body-only": "전개만 (도입/결론 없음)",
            },
            "intro_types": {
                "greeting": "인사/호칭 (안녕하세요, 여러분 등)",
                "self_intro": "자기소개 (저는, 나는 등)",
                "topic_present": "주제 제시 (오늘은, 이번에 등)",
                "context_setting": "배경 설정 (최근, 지난 등)",
                "question_intro": "질문형 도입 (혹시, 궁금 등)",
                "exclamatory_intro": "감탄/구어체 도입 (야, 아니 등)",
            },
            "conclusion_types": {
                "summary": "요약/정리",
                "cta": "행동 유도 (CTA)",
                "gratitude": "감사 표현",
                "closing_greeting": "이별 인사",
                "open_question": "개방형 질문 (커뮤니티 참여 유도)",
                "hope_expression": "기대/희망 표현",
                "signature": "서명/드림",
            },
            "body_types": {
                "narration": "서술 (경험, 사건, 에피소드)",
                "argument": "논증 (주장+근거)",
                "question": "질문 (물음표 기반)",
                "list": "목록 (번호, 불릿, 열거)",
                "code_block": "코드블록",
                "explanation": "설명 (개념, 정의, 해설)",
                "comparison": "비교 (장단점, A vs B)",
                "quotation": "인용 (다른 사람/글 인용)",
                "plain": "단순 텍스트 (특정 패턴 없음)",
            },
        },
        "overall": overall,
        "by_agent": by_agent,
        "by_submadang": by_submadang,
        "dsc_cross_reference": dsc_cross_ref,
        "post_details": results,
    }

    # 8. 저장
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2, default=str)
    logger.info(f"결과 저장: {OUTPUT_PATH.relative_to(PROJECT_ROOT)}")

    # 9. 요약 출력
    logger.info("=" * 60)
    logger.info("담화 구조 분석 완료 요약")
    logger.info("=" * 60)
    logger.info(f"  총 게시글: {len(results)}건")
    logger.info(f"  구조 유형 분포:")
    for st, info in overall["structure_type_distribution"].items():
        logger.info(f"    {st}: {info['count']}건 ({info['ratio']*100:.1f}%)")
    logger.info(f"  도입부 있는 글: {overall['intro']['posts_with_intro']}건 "
                f"({overall['intro']['ratio']*100:.1f}%)")
    logger.info(f"  결론부 있는 글: {overall['conclusion']['posts_with_conclusion']}건 "
                f"({overall['conclusion']['ratio']*100:.1f}%)")
    logger.info(f"  지배적 전개부 유형:")
    for bt, info in list(overall["body"]["dominant_type_distribution"].items())[:5]:
        logger.info(f"    {bt}: {info['count']}건 ({info['ratio']*100:.1f}%)")
    logger.info(f"  출력 파일: {OUTPUT_PATH.relative_to(PROJECT_ROOT)}")

    return output


if __name__ == "__main__":
    try:
        result = run_structure_analysis()
        print(f"\n담화 구조 분석 완료!")
        print(f"결과 파일: {OUTPUT_PATH}")
    except Exception as e:
        logger.error(f"분석 실행 실패: {e}", exc_info=True)
        sys.exit(1)
