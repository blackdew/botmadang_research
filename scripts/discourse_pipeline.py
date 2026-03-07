#!/usr/bin/env python3
"""봇마당 담화 분석 파이프라인

Fairclough CDA(비판적 담화 분석) 기반 다층 분석을 수행한다.
외부 NLP 라이브러리 없이 정규식 기반으로 한국어 텍스트를 분석한다.

분석 항목:
    1. 기초 텍스트 통계 (글 길이, 문장 수, 단어 수)
    2. 어휘 다양성 (Type-Token Ratio)
    3. 문체 분류 (존댓말/반말, 격식/비격식)
    4. AI스러움 지표 (과잉 정중, 템플릿 도입부, 면책 표현, 양시론)
    5. 마당별 비교
    6. 에이전트별 담화 프로필

사용법:
    python scripts/discourse_pipeline.py
    python scripts/discourse_pipeline.py --input data/raw/custom_posts.json
    python scripts/discourse_pipeline.py --output analysis/custom_output/
"""

import argparse
import json
import logging
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

# 프로젝트 루트를 sys.path에 추가
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from scripts.config import (
        PROCESSED_DATA_DIR,
        RAW_DATA_DIR,
    )
except ImportError:
    RAW_DATA_DIR = str(PROJECT_ROOT / "data" / "raw")
    PROCESSED_DATA_DIR = str(PROJECT_ROOT / "data" / "processed")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# 패턴 정의
# ──────────────────────────────────────────────────────────────────────────────

# 문장 분리: 마침표/느낌표/물음표 뒤 공백 또는 줄바꿈
SENTENCE_SPLIT_PATTERN = re.compile(r"[.!?。]\s+|[.!?。]$|\n{2,}")

# 단어 분리: 한국어 자모+한글, 영문, 숫자 단위 토큰화 (조사 부착 형태 유지)
WORD_PATTERN = re.compile(r"[가-힣a-zA-Z0-9]+")

# ── 존댓말 종결어미 패턴 ──
# 합쇼체: -습니다/-ㅂ니다/-십니다/-십시오/-세요/-해요/-아요/-어요/-네요 등
FORMAL_POLITE_ENDINGS = re.compile(
    r"(습니다|ㅂ니다|십니다|십시오|시오|세요|해요|아요|어요|네요|죠|군요|겠습니다|했습니다|됩니다|됩니까|입니까|으로서|으시기|드립니다|감사합니다|부탁드립니다|알려드립니다|확인해보세요|해보세요|보세요)[.?!,\s]"
)
# 해체/반말: -다/-야/-지/-냐/-나/-거든/-잖아/-는데/-뭐 등
INFORMAL_ENDINGS = re.compile(
    r"(이야|거야|다고|하다|했다|한다|됐다|됩다|이다|였다|이었다|는다|ㄴ다|해|야|지|냐|나|거든|잖아|는데|뭐)[.!?\s]"
)
# 해요체가 없고 반말 패턴만 있을 때 반말로 분류

# ── 격식 마커 ──
FORMAL_MARKERS = re.compile(
    r"(안녕하세요|안녕히 가세요|감사합니다|부탁드립니다|실례지만|말씀드립니다|여쭤보겠습니다|이하와 같이|다음과 같이|귀사|귀하|저희|본인|당사)"
)
INFORMAL_MARKERS = re.compile(
    r"(ㅋㅋ|ㅎㅎ|ㅠㅠ|ㅜㅜ|ㄷㄷ|ㄴㄴ|ㅇㅇ|헐|대박|진짜|완전|넘|너무너무|ㅠ|ㅜ|!!|!!|👍|😊|🤣|😅|맞지\?|그렇지\?|어때\?)"
)

# ── AI스러움 지표 패턴 ──
AI_PATTERNS = {
    # 과잉 정중: "도움이 되셨으면", "궁금한 점이 있으시면" 등
    # 실제 데이터 기반으로 확장: 열린 질문 유도, 추가 도움 오퍼 등
    "over_polite": re.compile(
        r"(도움이 되셨으면|도움이 되길|도움이 되길 바|"
        r"궁금한 점이 있으시면|궁금하신 점|궁금한 점은|"
        r"언제든지 문의|언제든지 질문|더 궁금하신|도움이 필요하시면|"
        r"참고가 되셨으면|유익한 정보가 되셨으면|함께 나눌 수 있어|"
        r"더 자세한 내용이 필요하시면|추가적인 도움|더 알고 싶으시다면|"
        r"도움이 되었으면|도움이 되었기를|도움 되셨으면|"
        r"여러분도 한번|여러분은 어떻게|여러분의 생각은|여러분은 어떻|"
        r"어떻게 생각하시나요|어떻게 생각하세요|여러분만의)"
    ),
    # 템플릿 도입부: "~에 대해 알아보겠습니다", "오늘은 ~에 대해" 등
    # '오늘은' 단독 도입부는 일상 표현이므로 제외, 정보 제공 의도 패턴만 포함
    "template_intro": re.compile(
        r"(오늘은.{0,30}에 대해|오늘.{0,20}알아보겠|오늘은.{0,30}소개해|"
        r"에 대해 알아보겠습니다|에 대해 살펴보겠습니다|에 대해 설명해드리겠습니다|"
        r"에 대해 정리해보겠습니다|에 대해 이야기해보겠습니다|"
        r"이번에는.{0,30}에 대해|이번 글에서는|이번 포스팅에서는|"
        r"안녕하세요.{0,50}입니다|반갑습니다.{0,50}입니다|"
        r"특별히.{0,30}소개|오늘 소개해드릴|오늘 알아볼)"
    ),
    # 면책 표현: "정확하지 않을 수 있", "참고만 하시", "전문가 상담 권장" 등
    "disclaimer": re.compile(
        r"(정확하지 않을 수|정확하지 않을 수도|오류가 있을 수|"
        r"참고로만|참고만 하시|참고용으로|전문가와 상담|전문가에게 문의|"
        r"투자에 주의|투자 손실|이 글은.{0,30}아닙니다|"
        r"개인적인 의견|제 생각일 뿐|틀릴 수 있습니다|"
        r"최신 정보가 아닐|변경될 수 있습니다|최종 결정은.{0,20}하세요|"
        r"투자 판단은|법적 책임|책임지지 않습니다|책임지지 않으며)"
    ),
    # 양시론: "한편으로는", "반면에" 등 균형 잡힌 구조
    "both_sides": re.compile(
        r"(한편으로는|한편으로|반면에|반면|"
        r"장점이 있는 반면|단점도 있|긍정적인 면|부정적인 면|"
        r"일장일단|균형 잡힌|두 가지 측면|양면이|pros and cons|"
        r"이점이 있지만.{0,30}단점|좋은 점도 있지만|"
        r"장점은.{0,50}단점|단점은.{0,50}장점)"
    ),
    # 열거 패턴: "첫째", "첫 번째" 등 목록형 구조 (AI 특유)
    "list_structure": re.compile(
        r"(첫째|첫 번째|1\.|①|1\)|둘째|두 번째|2\.|②|2\)|"
        r"셋째|세 번째|3\.|③|3\)|마지막으로|요약하자면|정리하자면)"
    ),
}

# ── 추가 AI 특징 패턴 ──
AI_TOPIC_MARKERS = re.compile(
    r"(핵심은|중요한 것은|결론적으로|결국|요컨대|즉|다시 말해|"
    r"정리하면|요약하면|한 마디로|결론은|따라서|그러므로)"
)

# ──────────────────────────────────────────────────────────────────────────────
# 분석 함수
# ──────────────────────────────────────────────────────────────────────────────


def split_sentences(text: str) -> list[str]:
    """문장 분리 (정규식 기반)"""
    if not text:
        return []
    # 줄바꿈을 마침표처럼 처리
    text_normalized = text.replace("\n\n", ". ").replace("\n", " ")
    parts = re.split(r"(?<=[.!?])\s+|(?<=[。！？])", text_normalized)
    sentences = [s.strip() for s in parts if s.strip() and len(s.strip()) > 1]
    return sentences


def tokenize(text: str) -> list[str]:
    """단어 토큰화 (정규식 기반)"""
    if not text:
        return []
    return WORD_PATTERN.findall(text)


def compute_ttr(tokens: list[str]) -> float:
    """Type-Token Ratio 계산: 고유 단어 수 / 전체 단어 수"""
    if not tokens:
        return 0.0
    types = set(t.lower() for t in tokens)
    return round(len(types) / len(tokens), 4)


def classify_speech_level(text: str) -> dict[str, Any]:
    """존댓말/반말 및 격식/비격식 분류"""
    if not text:
        return {
            "honorific": "unknown",
            "formality": "unknown",
            "honorific_count": 0,
            "informal_count": 0,
            "formal_marker_count": 0,
            "informal_marker_count": 0,
        }

    honorific_matches = FORMAL_POLITE_ENDINGS.findall(text)
    informal_matches = INFORMAL_ENDINGS.findall(text)
    formal_marker_matches = FORMAL_MARKERS.findall(text)
    informal_marker_matches = INFORMAL_MARKERS.findall(text)

    h_count = len(honorific_matches)
    i_count = len(informal_matches)
    fm_count = len(formal_marker_matches)
    im_count = len(informal_marker_matches)

    # 존댓말 여부 판별: 존댓말 패턴이 더 많으면 존댓말
    if h_count > i_count:
        honorific = "honorific"
    elif i_count > h_count:
        honorific = "informal"
    elif h_count == 0 and i_count == 0:
        # 패턴 매칭 안 됨 → 내용 기반 추정
        honorific = "neutral"
    else:
        honorific = "mixed"

    # 격식 판별
    if fm_count > im_count * 2:
        formality = "formal"
    elif im_count > fm_count:
        formality = "informal"
    else:
        formality = "semi-formal"

    return {
        "honorific": honorific,
        "formality": formality,
        "honorific_count": h_count,
        "informal_count": i_count,
        "formal_marker_count": fm_count,
        "informal_marker_count": im_count,
    }


def compute_ai_indicators(text: str) -> dict[str, Any]:
    """AI스러움 지표 계산"""
    if not text:
        return {k: {"count": 0, "matches": []} for k in AI_PATTERNS}

    result = {}
    total_score = 0.0

    for indicator_name, pattern in AI_PATTERNS.items():
        matches = pattern.findall(text)
        count = len(matches)
        result[indicator_name] = {
            "count": count,
            "matches": matches[:5],  # 최대 5개 예시 저장
        }
        total_score += count

    # 토픽 마커 (별도 집계)
    topic_matches = AI_TOPIC_MARKERS.findall(text)
    result["topic_markers"] = {
        "count": len(topic_matches),
        "matches": topic_matches[:5],
    }
    total_score += len(topic_matches)

    # AI 지수: 패턴 발화 수 / 문장 수 (0~1 정규화)
    sentences = split_sentences(text)
    sentence_count = max(len(sentences), 1)
    ai_density = min(total_score / sentence_count, 1.0)

    result["ai_score"] = round(ai_density, 4)
    result["total_pattern_count"] = int(total_score)

    return result


def analyze_post(post: dict) -> dict[str, Any]:
    """단일 게시글 전체 분석"""
    content = post.get("content", "") or ""
    title = post.get("title", "") or ""
    full_text = (title + " " + content).strip()

    tokens = tokenize(content)
    sentences = split_sentences(content)
    words_count = len(tokens)
    sentence_count = len(sentences)
    char_count = len(content)

    ttr = compute_ttr(tokens)
    speech = classify_speech_level(content)
    ai_ind = compute_ai_indicators(content)

    # 평균 문장 길이 (단어 수 기준)
    avg_sent_len = round(words_count / max(sentence_count, 1), 2)

    return {
        "id": post.get("id", ""),
        "author_id": post.get("author_id", ""),
        "author_name": post.get("author_name", ""),
        "submadang": post.get("submadang", ""),
        "created_at": post.get("created_at", ""),
        "upvotes": post.get("upvotes", 0),
        "downvotes": post.get("downvotes", 0),
        "comment_count": post.get("comment_count", 0),
        "basic_stats": {
            "char_count": char_count,
            "word_count": words_count,
            "sentence_count": sentence_count,
            "avg_sentence_length_words": avg_sent_len,
            "title_length": len(title),
        },
        "ttr": ttr,
        "speech_level": speech,
        "ai_indicators": ai_ind,
    }


# ──────────────────────────────────────────────────────────────────────────────
# 집계 함수
# ──────────────────────────────────────────────────────────────────────────────


def aggregate_basic_stats(analyzed: list[dict]) -> dict[str, Any]:
    """기초 통계 집계"""
    if not analyzed:
        return {}

    char_counts = [a["basic_stats"]["char_count"] for a in analyzed]
    word_counts = [a["basic_stats"]["word_count"] for a in analyzed]
    sent_counts = [a["basic_stats"]["sentence_count"] for a in analyzed]

    def stats_dict(values: list[float]) -> dict:
        if not values:
            return {}
        sorted_v = sorted(values)
        n = len(sorted_v)
        mean = sum(sorted_v) / n
        median = sorted_v[n // 2] if n % 2 == 1 else (sorted_v[n // 2 - 1] + sorted_v[n // 2]) / 2
        variance = sum((x - mean) ** 2 for x in sorted_v) / n
        std = variance ** 0.5
        q1 = sorted_v[n // 4]
        q3 = sorted_v[3 * n // 4]
        return {
            "count": n,
            "mean": round(mean, 2),
            "median": round(median, 2),
            "std": round(std, 2),
            "min": sorted_v[0],
            "max": sorted_v[-1],
            "q1": q1,
            "q3": q3,
        }

    # 마당별 분포
    submadang_counts: Counter = Counter(a["submadang"] for a in analyzed)
    # 작성자별 분포
    author_counts: Counter = Counter(a["author_name"] for a in analyzed)

    return {
        "total_posts": len(analyzed),
        "char_count_distribution": stats_dict(char_counts),
        "word_count_distribution": stats_dict(word_counts),
        "sentence_count_distribution": stats_dict(sent_counts),
        "submadang_distribution": dict(submadang_counts.most_common()),
        "author_distribution": dict(author_counts.most_common()),
        "generated_at": datetime.now().isoformat(),
    }


def aggregate_ttr_by_agent(analyzed: list[dict]) -> dict[str, Any]:
    """에이전트별 TTR 집계"""
    agent_tokens: dict[str, list[str]] = defaultdict(list)

    # 에이전트별 전체 토큰 풀 합산 (누적 TTR이 더 안정적)
    for a in analyzed:
        name = a["author_name"]
        agent_tokens[name]  # 초기화

    # 게시글별 TTR도 수집
    agent_post_ttrs: dict[str, list[float]] = defaultdict(list)
    agent_post_counts: Counter = Counter()

    for a in analyzed:
        name = a["author_name"]
        agent_post_ttrs[name].append(a["ttr"])
        agent_post_counts[name] += 1

    # 에이전트별 원본 텍스트로 누적 TTR 계산을 위해 별도 처리
    result = {}
    for name in sorted(agent_post_counts.keys(), key=lambda x: -agent_post_counts[x]):
        ttrs = agent_post_ttrs[name]
        n = len(ttrs)
        mean_ttr = round(sum(ttrs) / n, 4) if n > 0 else 0.0
        sorted_ttrs = sorted(ttrs)
        median_ttr = sorted_ttrs[n // 2] if n % 2 == 1 else round(
            (sorted_ttrs[n // 2 - 1] + sorted_ttrs[n // 2]) / 2, 4
        )
        result[name] = {
            "post_count": n,
            "mean_ttr": mean_ttr,
            "median_ttr": median_ttr,
            "min_ttr": sorted_ttrs[0] if sorted_ttrs else 0,
            "max_ttr": sorted_ttrs[-1] if sorted_ttrs else 0,
        }

    return {
        "ttr_by_agent": result,
        "note": "TTR = Type-Token Ratio (고유 단어 수 / 전체 단어 수). 높을수록 어휘가 다양함.",
        "generated_at": datetime.now().isoformat(),
    }


def aggregate_style_analysis(analyzed: list[dict]) -> dict[str, Any]:
    """문체 분석 집계"""
    honorific_counter: Counter = Counter()
    formality_counter: Counter = Counter()

    # 에이전트별 문체 분포
    agent_style: dict[str, dict] = defaultdict(
        lambda: {
            "honorific_counts": Counter(),
            "formality_counts": Counter(),
            "post_count": 0,
        }
    )

    for a in analyzed:
        sl = a["speech_level"]
        honorific_counter[sl["honorific"]] += 1
        formality_counter[sl["formality"]] += 1

        name = a["author_name"]
        agent_style[name]["honorific_counts"][sl["honorific"]] += 1
        agent_style[name]["formality_counts"][sl["formality"]] += 1
        agent_style[name]["post_count"] += 1

    # 에이전트별 주요 문체 결정 (최빈값)
    agent_style_summary = {}
    for name, data in agent_style.items():
        dominant_honorific = data["honorific_counts"].most_common(1)[0][0]
        dominant_formality = data["formality_counts"].most_common(1)[0][0]
        agent_style_summary[name] = {
            "post_count": data["post_count"],
            "dominant_honorific": dominant_honorific,
            "dominant_formality": dominant_formality,
            "honorific_distribution": dict(data["honorific_counts"]),
            "formality_distribution": dict(data["formality_counts"]),
        }

    return {
        "overall_honorific_distribution": dict(honorific_counter),
        "overall_formality_distribution": dict(formality_counter),
        "agent_style_summary": agent_style_summary,
        "label_description": {
            "honorific": {
                "honorific": "존댓말 (합쇼체/해요체 종결어미 우세)",
                "informal": "반말 (해체/해라체 종결어미 우세)",
                "mixed": "혼합 (존댓말+반말 공존)",
                "neutral": "중립 (종결어미 패턴 불명확)",
            },
            "formality": {
                "formal": "격식체",
                "semi-formal": "준격식체",
                "informal": "비격식체",
            },
        },
        "generated_at": datetime.now().isoformat(),
    }


def aggregate_ai_indicators(analyzed: list[dict]) -> dict[str, Any]:
    """AI스러움 지표 집계"""
    indicator_names = list(AI_PATTERNS.keys()) + ["topic_markers"]

    # 전체 집계
    overall: dict[str, int] = defaultdict(int)
    ai_scores = []

    # 에이전트별 집계
    agent_ai: dict[str, dict] = defaultdict(
        lambda: {ind: 0 for ind in indicator_names} | {"post_count": 0, "ai_score_sum": 0.0}
    )

    for a in analyzed:
        ai_ind = a["ai_indicators"]
        ai_scores.append(ai_ind.get("ai_score", 0.0))
        name = a["author_name"]
        agent_ai[name]["post_count"] += 1
        agent_ai[name]["ai_score_sum"] += ai_ind.get("ai_score", 0.0)

        for ind in indicator_names:
            if ind in ai_ind:
                count = ai_ind[ind].get("count", 0)
                overall[ind] += count
                agent_ai[name][ind] += count

    # 에이전트별 평균 AI 점수
    agent_ai_summary = {}
    for name, data in sorted(agent_ai.items(), key=lambda x: -x[1]["post_count"]):
        post_count = data["post_count"]
        avg_score = round(data["ai_score_sum"] / max(post_count, 1), 4)
        agent_ai_summary[name] = {
            "post_count": post_count,
            "avg_ai_score": avg_score,
            "indicator_totals": {ind: data[ind] for ind in indicator_names},
            "indicator_per_post": {
                ind: round(data[ind] / max(post_count, 1), 3)
                for ind in indicator_names
            },
        }

    # 전체 평균 AI 점수
    overall_avg = round(sum(ai_scores) / max(len(ai_scores), 1), 4)

    # 상위 AI 지수 에이전트 (게시글 5개 이상)
    top_ai_agents = sorted(
        [(name, d["avg_ai_score"]) for name, d in agent_ai_summary.items() if d["post_count"] >= 5],
        key=lambda x: -x[1],
    )

    return {
        "overall_avg_ai_score": overall_avg,
        "overall_indicator_totals": dict(overall),
        "agent_ai_summary": agent_ai_summary,
        "top_ai_score_agents": [{"name": n, "avg_ai_score": s} for n, s in top_ai_agents],
        "indicator_descriptions": {
            "over_polite": "과잉 정중 표현 (헬프 오퍼, 추가 문의 유도 등)",
            "template_intro": "템플릿식 도입부 ('오늘은 ~에 대해', '~알아보겠습니다' 등)",
            "disclaimer": "면책 표현 ('정확하지 않을 수 있음', '전문가 상담 권장' 등)",
            "both_sides": "양시론적 구조 ('한편', '반면에', 장단점 나열 등)",
            "list_structure": "열거 구조 ('첫째', '1.', '①' 등 목록형 정리)",
            "topic_markers": "주제 전환 마커 ('결론적으로', '즉', '요컨대' 등)",
            "ai_score": "AI 밀도 지수 = 패턴 발화 수 / 문장 수 (0~1)",
        },
        "generated_at": datetime.now().isoformat(),
    }


def aggregate_submadang_comparison(analyzed: list[dict]) -> dict[str, Any]:
    """마당별 담화 특성 비교 집계"""
    madang_data: dict[str, dict] = defaultdict(
        lambda: {
            "post_count": 0,
            "unique_authors": set(),
            "char_counts": [],
            "word_counts": [],
            "ttr_values": [],
            "honorific_counts": Counter(),
            "formality_counts": Counter(),
            "ai_scores": [],
            "ai_indicators": defaultdict(int),
            "total_upvotes": 0,
            "total_comments": 0,
        }
    )

    indicator_names = list(AI_PATTERNS.keys()) + ["topic_markers"]

    for a in analyzed:
        m = a["submadang"]
        d = madang_data[m]
        d["post_count"] += 1
        d["unique_authors"].add(a["author_name"])
        d["char_counts"].append(a["basic_stats"]["char_count"])
        d["word_counts"].append(a["basic_stats"]["word_count"])
        d["ttr_values"].append(a["ttr"])
        d["honorific_counts"][a["speech_level"]["honorific"]] += 1
        d["formality_counts"][a["speech_level"]["formality"]] += 1
        d["ai_scores"].append(a["ai_indicators"].get("ai_score", 0.0))
        d["total_upvotes"] += a.get("upvotes", 0)
        d["total_comments"] += a.get("comment_count", 0)
        for ind in indicator_names:
            if ind in a["ai_indicators"]:
                d["ai_indicators"][ind] += a["ai_indicators"][ind].get("count", 0)

    def mean(values: list) -> float:
        return round(sum(values) / max(len(values), 1), 2)

    result = {}
    for madang, d in sorted(madang_data.items(), key=lambda x: -x[1]["post_count"]):
        n = d["post_count"]
        result[madang] = {
            "post_count": n,
            "unique_author_count": len(d["unique_authors"]),
            "unique_authors": sorted(d["unique_authors"]),
            "avg_char_count": mean(d["char_counts"]),
            "avg_word_count": mean(d["word_counts"]),
            "avg_ttr": mean(d["ttr_values"]),
            "avg_ai_score": mean(d["ai_scores"]),
            "dominant_honorific": d["honorific_counts"].most_common(1)[0][0] if d["honorific_counts"] else "unknown",
            "honorific_distribution": dict(d["honorific_counts"]),
            "formality_distribution": dict(d["formality_counts"]),
            "ai_indicator_totals": dict(d["ai_indicators"]),
            "ai_indicator_per_post": {
                ind: round(d["ai_indicators"][ind] / max(n, 1), 3)
                for ind in indicator_names
            },
            "total_upvotes": d["total_upvotes"],
            "avg_upvotes": round(d["total_upvotes"] / max(n, 1), 2),
            "total_comments": d["total_comments"],
            "avg_comments": round(d["total_comments"] / max(n, 1), 2),
        }

    return {
        "submadang_comparison": result,
        "generated_at": datetime.now().isoformat(),
    }


def aggregate_agent_profiles(analyzed: list[dict]) -> dict[str, Any]:
    """에이전트별 담화 프로필 생성"""
    agent_data: dict[str, dict] = defaultdict(
        lambda: {
            "author_id": "",
            "post_count": 0,
            "submadangs": Counter(),
            "char_counts": [],
            "word_counts": [],
            "ttr_values": [],
            "honorific_counts": Counter(),
            "formality_counts": Counter(),
            "ai_scores": [],
            "ai_indicators": defaultdict(int),
            "total_upvotes": 0,
            "total_comments": 0,
            "dates": [],
        }
    )

    indicator_names = list(AI_PATTERNS.keys()) + ["topic_markers"]

    for a in analyzed:
        name = a["author_name"]
        d = agent_data[name]
        if not d["author_id"]:
            d["author_id"] = a["author_id"]
        d["post_count"] += 1
        d["submadangs"][a["submadang"]] += 1
        d["char_counts"].append(a["basic_stats"]["char_count"])
        d["word_counts"].append(a["basic_stats"]["word_count"])
        d["ttr_values"].append(a["ttr"])
        d["honorific_counts"][a["speech_level"]["honorific"]] += 1
        d["formality_counts"][a["speech_level"]["formality"]] += 1
        d["ai_scores"].append(a["ai_indicators"].get("ai_score", 0.0))
        d["total_upvotes"] += a.get("upvotes", 0)
        d["total_comments"] += a.get("comment_count", 0)
        if a.get("created_at"):
            d["dates"].append(a["created_at"])
        for ind in indicator_names:
            if ind in a["ai_indicators"]:
                d["ai_indicators"][ind] += a["ai_indicators"][ind].get("count", 0)

    def mean(values: list) -> float:
        return round(sum(values) / max(len(values), 1), 2)

    def derive_discourse_style(d: dict, n: int) -> str:
        """담화 스타일 레이블 도출"""
        avg_ai = mean(d["ai_scores"])
        dominant_h = d["honorific_counts"].most_common(1)[0][0] if d["honorific_counts"] else "neutral"
        avg_word = mean(d["word_counts"])

        style_parts = []

        # 문체
        if dominant_h == "honorific":
            style_parts.append("존댓말")
        elif dominant_h == "informal":
            style_parts.append("반말")
        else:
            style_parts.append("혼합체")

        # 글 길이
        if avg_word > 200:
            style_parts.append("장문형")
        elif avg_word < 80:
            style_parts.append("단문형")
        else:
            style_parts.append("중문형")

        # AI 지수
        if avg_ai > 0.3:
            style_parts.append("AI형 담화")
        elif avg_ai > 0.1:
            style_parts.append("준AI형 담화")
        else:
            style_parts.append("자연형 담화")

        return " / ".join(style_parts)

    result = {}
    for name, d in sorted(agent_data.items(), key=lambda x: -x[1]["post_count"]):
        n = d["post_count"]
        avg_ai = mean(d["ai_scores"])

        # 주요 AI 지표 상위 2개 도출
        ind_per_post = {
            ind: round(d["ai_indicators"][ind] / max(n, 1), 3)
            for ind in indicator_names
        }
        top_indicators = sorted(
            [(k, v) for k, v in ind_per_post.items() if v > 0],
            key=lambda x: -x[1],
        )[:3]

        result[name] = {
            "author_id": d["author_id"],
            "post_count": n,
            "active_submadangs": dict(d["submadangs"].most_common()),
            "primary_submadang": d["submadangs"].most_common(1)[0][0] if d["submadangs"] else "unknown",
            "avg_char_count": mean(d["char_counts"]),
            "avg_word_count": mean(d["word_counts"]),
            "avg_ttr": mean(d["ttr_values"]),
            "avg_ai_score": round(avg_ai, 4),
            "dominant_honorific": d["honorific_counts"].most_common(1)[0][0] if d["honorific_counts"] else "unknown",
            "dominant_formality": d["formality_counts"].most_common(1)[0][0] if d["formality_counts"] else "unknown",
            "honorific_distribution": dict(d["honorific_counts"]),
            "formality_distribution": dict(d["formality_counts"]),
            "ai_indicator_per_post": ind_per_post,
            "top_ai_indicators": [{"indicator": k, "per_post": v} for k, v in top_indicators],
            "total_upvotes": d["total_upvotes"],
            "avg_upvotes": round(d["total_upvotes"] / max(n, 1), 2),
            "total_comments": d["total_comments"],
            "avg_comments": round(d["total_comments"] / max(n, 1), 2),
            "discourse_style_label": derive_discourse_style(d, n),
            "activity_period": {
                "first_post": min(d["dates"]) if d["dates"] else None,
                "last_post": max(d["dates"]) if d["dates"] else None,
            },
        }

    return {
        "agent_discourse_profiles": result,
        "total_agents": len(result),
        "generated_at": datetime.now().isoformat(),
    }


# ──────────────────────────────────────────────────────────────────────────────
# I/O 유틸리티
# ──────────────────────────────────────────────────────────────────────────────


def load_posts(input_path: str) -> list[dict]:
    """게시글 JSON 로드"""
    logger.info(f"데이터 로드: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    # {"posts": [...]} 형태 지원
    if isinstance(data, dict) and "posts" in data:
        return data["posts"]
    raise ValueError(f"지원하지 않는 데이터 형식: {type(data)}")


def save_json(data: Any, filepath: str) -> None:
    """JSON 파일 저장"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    logger.info(f"  저장 완료: {os.path.relpath(filepath)}")


# ──────────────────────────────────────────────────────────────────────────────
# 메인 파이프라인
# ──────────────────────────────────────────────────────────────────────────────


def run_pipeline(input_path: str, output_dir: str) -> dict[str, str]:
    """담화 분석 파이프라인 전체 실행"""
    logger.info("=" * 60)
    logger.info("봇마당 담화 분석 파이프라인 시작 (Fairclough CDA 기반)")
    logger.info("=" * 60)

    # ── 1. 데이터 로드 ──
    posts = load_posts(input_path)
    logger.info(f"게시글 {len(posts)}개 로드 완료")

    # ── 2. 게시글별 분석 ──
    logger.info("개별 게시글 분석 중...")
    analyzed = []
    for i, post in enumerate(posts):
        if (i + 1) % 100 == 0:
            logger.info(f"  진행: {i + 1}/{len(posts)}")
        analyzed.append(analyze_post(post))
    logger.info(f"게시글 {len(analyzed)}개 분석 완료")

    # ── 3. 각 분석 집계 및 저장 ──
    output_files = {}

    # 3-1. 기초 통계
    logger.info("기초 통계 집계...")
    basic_stats = aggregate_basic_stats(analyzed)
    out_path = os.path.join(output_dir, "basic_stats.json")
    save_json(basic_stats, out_path)
    output_files["basic_stats"] = out_path

    # 3-2. TTR
    logger.info("어휘 다양성(TTR) 집계...")
    ttr_data = aggregate_ttr_by_agent(analyzed)
    out_path = os.path.join(output_dir, "ttr_by_agent.json")
    save_json(ttr_data, out_path)
    output_files["ttr_by_agent"] = out_path

    # 3-3. 문체 분석
    logger.info("문체 분석 집계...")
    style_data = aggregate_style_analysis(analyzed)
    out_path = os.path.join(output_dir, "style_analysis.json")
    save_json(style_data, out_path)
    output_files["style_analysis"] = out_path

    # 3-4. AI 지표
    logger.info("AI스러움 지표 집계...")
    ai_data = aggregate_ai_indicators(analyzed)
    out_path = os.path.join(output_dir, "ai_indicators.json")
    save_json(ai_data, out_path)
    output_files["ai_indicators"] = out_path

    # 3-5. 마당별 비교
    logger.info("마당별 비교 집계...")
    submadang_data = aggregate_submadang_comparison(analyzed)
    out_path = os.path.join(output_dir, "submadang_comparison.json")
    save_json(submadang_data, out_path)
    output_files["submadang_comparison"] = out_path

    # 3-6. 에이전트 프로필
    logger.info("에이전트별 담화 프로필 생성...")
    profiles_data = aggregate_agent_profiles(analyzed)
    out_path = os.path.join(output_dir, "agent_discourse_profiles.json")
    save_json(profiles_data, out_path)
    output_files["agent_discourse_profiles"] = out_path

    # ── 4. 요약 출력 ──
    logger.info("=" * 60)
    logger.info("분석 완료 요약")
    logger.info("=" * 60)
    logger.info(f"  총 게시글: {len(posts)}개")
    logger.info(f"  마당 수: {len(basic_stats.get('submadang_distribution', {}))}")
    logger.info(f"  에이전트 수: {profiles_data.get('total_agents', 0)}")
    logger.info(f"  출력 디렉토리: {output_dir}")
    for name, path in output_files.items():
        logger.info(f"    - {name}: {os.path.relpath(path)}")

    return output_files


def main():
    parser = argparse.ArgumentParser(
        description="봇마당 담화 분석 파이프라인 (Fairclough CDA 기반)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python scripts/discourse_pipeline.py
  python scripts/discourse_pipeline.py --input data/raw/custom_posts.json
  python scripts/discourse_pipeline.py --output analysis/custom_output/
        """,
    )
    parser.add_argument(
        "--input",
        default=os.path.join(RAW_DATA_DIR, "pilot_posts.json"),
        help=f"입력 JSON 파일 경로 (기본값: {os.path.join(RAW_DATA_DIR, 'pilot_posts.json')})",
    )
    parser.add_argument(
        "--output",
        default=str(PROJECT_ROOT / "analysis" / "discourse"),
        help="출력 디렉토리 경로 (기본값: analysis/discourse/)",
    )
    args = parser.parse_args()

    if not os.path.exists(args.input):
        logger.error(f"입력 파일을 찾을 수 없습니다: {args.input}")
        sys.exit(1)

    try:
        output_files = run_pipeline(args.input, args.output)
        print(f"\n담화 분석 파이프라인 완료!")
        print(f"출력 파일 ({len(output_files)}개):")
        for name, path in output_files.items():
            print(f"  - {os.path.relpath(path)}")
    except Exception as e:
        logger.error(f"파이프라인 실행 실패: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
