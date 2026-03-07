#!/usr/bin/env python3
"""봇마당 에이전트 페르소나 프로파일러

Goffman 자기표현론 기반으로 에이전트별 페르소나를 분석한다.
외부 NLP 라이브러리 없이 정규식과 통계 연산만 사용한다.

사용법:
    python scripts/profiler.py
    python scripts/profiler.py --output analysis/profiles/
    python scripts/profiler.py --posts data/raw/pilot_posts.json
"""

import argparse
import json
import logging
import math
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# 프로젝트 루트를 sys.path에 추가
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# 경로 상수
# ──────────────────────────────────────────────
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
ANALYSIS_PROFILES_DIR = os.path.join(PROJECT_ROOT, "analysis", "profiles")


# ──────────────────────────────────────────────
# 마당 분류 상수
# ──────────────────────────────────────────────
TECH_SUBMADANGS = {"tech", "vibecoding", "edutech", "showcase"}
SOCIAL_SUBMADANGS = {"daily", "cute_ai", "korea", "classical_music"}
INTELLECTUAL_SUBMADANGS = {"philosophy", "general", "questions"}
FINANCE_SUBMADANGS = {"finance"}

# 페르소나 유형 상수
PERSONA_EXPERT = "PER-EXPERT"
PERSONA_FRIENDLY = "PER-FRIENDLY"
PERSONA_HUMOROUS = "PER-HUMOROUS"
PERSONA_SERIOUS = "PER-SERIOUS"
PERSONA_CURIOUS = "PER-CURIOUS"
PERSONA_HELPER = "PER-HELPER"


# ──────────────────────────────────────────────
# 텍스트 분석 유틸리티
# ──────────────────────────────────────────────

def count_chars(text: str) -> int:
    """텍스트 길이(공백 제외 문자 수)"""
    return len(text.replace(" ", "").replace("\n", ""))


def has_honorific(text: str) -> bool:
    """존댓말 사용 여부 판별

    '-요', '-습니다', '-세요', '-셨', '-시면' 등으로 끝나는 패턴 탐지.
    """
    honorific_patterns = [
        r"습니다[.\s!?]",
        r"입니다[.\s!?]",
        r"[가-힣]요[.\s!?]",
        r"[가-힣]요$",
        r"세요[.\s!?]",
        r"셨[가-힣]*[.\s!?]",
        r"십니다",
        r"겠습니다",
        r"드립니다",
        r"했습니다",
        r"있습니다",
        r"됩니다",
        r"합니다",
    ]
    for pat in honorific_patterns:
        if re.search(pat, text):
            return True
    return False


def count_question_marks(text: str) -> int:
    """물음표 개수 (한국어 '?' 및 '？' 포함)"""
    return text.count("?") + text.count("？")


def count_humor_markers(text: str) -> int:
    """유머 마커 개수: ㅋ, ㅎ, 이모지, ^^, ~~ 등"""
    patterns = [
        r"ㅋ+",
        r"ㅎ+",
        r"ㅠ+",
        r"ㅜ+",
        r"[😂🤣😄😃😁😆😅🙂😊😀🎉🚀💡✅☑️👍👏🙏💪]",
        r"\^\^+",
        r"~~+",
        r"\.\.\.+",
    ]
    count = 0
    for pat in patterns:
        count += len(re.findall(pat, text))
    return count


def count_helper_markers(text: str) -> int:
    """도우미 마커: 안내, 설명, 추천, '~하면', '~하시면' 등"""
    patterns = [
        r"추천",
        r"안내",
        r"알려드",
        r"참고",
        r"도움",
        r"방법",
        r"정보",
        r"활용",
        r"확인",
        r"서비스",
        r"툴",
        r"무료",
        r"링크",
    ]
    count = 0
    for pat in patterns:
        count += len(re.findall(pat, text))
    return count


def detect_argumentative(text: str) -> bool:
    """논증적 패턴 탐지: '따라서', '결국', '왜냐하면', '근거' 등"""
    patterns = [
        r"따라서",
        r"결국",
        r"왜냐하면",
        r"근거",
        r"첫째",
        r"둘째",
        r"셋째",
        r"반면",
        r"그러나",
        r"하지만",
        r"즉,",
        r"즉 ",
        r"결론",
        r"논리",
        r"분석",
        r"관점",
        r"핵심은",
    ]
    count = sum(1 for p in patterns if re.search(p, text))
    return count >= 2


def stddev(values: list[float]) -> float:
    """표준편차 계산"""
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    return math.sqrt(variance)


def safe_mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


# ──────────────────────────────────────────────
# 데이터 로딩
# ──────────────────────────────────────────────

def load_posts(posts_path: str) -> list[dict]:
    """게시글 JSON 파일 로드"""
    with open(posts_path, encoding="utf-8") as f:
        posts = json.load(f)
    logger.info(f"게시글 {len(posts)}개 로드 완료: {posts_path}")
    return posts


def load_comments(raw_dir: str) -> dict[str, list[dict]]:
    """에이전트별 댓글 파일 로드

    Returns:
        {author_name: [comment, ...]} 형태의 딕셔너리
    """
    comments_by_agent: dict[str, list[dict]] = {}
    pattern = re.compile(r"agent_(.+)_comments\.json$")
    raw_path = Path(raw_dir)

    for fpath in raw_path.glob("agent_*_comments.json"):
        match = pattern.match(fpath.name)
        if not match:
            continue
        agent_name = match.group(1)
        with open(fpath, encoding="utf-8") as f:
            comments = json.load(f)
        comments_by_agent[agent_name] = comments
        logger.info(f"  댓글 로드: {agent_name} ({len(comments)}개)")

    logger.info(f"댓글 파일 {len(comments_by_agent)}개 로드 완료")
    return comments_by_agent


def load_agent_summary(summary_path: str) -> dict[str, dict]:
    """에이전트 요약 JSON 로드

    Returns:
        {author_id: agent_summary} 딕셔너리
    """
    with open(summary_path, encoding="utf-8") as f:
        summaries = json.load(f)

    by_id = {s["author_id"]: s for s in summaries}
    logger.info(f"에이전트 요약 {len(by_id)}개 로드 완료")
    return by_id


# ──────────────────────────────────────────────
# 에이전트별 데이터 집계
# ──────────────────────────────────────────────

def group_posts_by_agent(posts: list[dict]) -> dict[str, dict]:
    """게시글을 에이전트 ID 기준으로 분류

    Returns:
        {author_id: {"name": str, "posts": [post, ...]}}
    """
    grouped: dict[str, dict] = {}
    for post in posts:
        aid = post["author_id"]
        if aid not in grouped:
            grouped[aid] = {"name": post["author_name"], "posts": []}
        grouped[aid]["posts"].append(post)
    return grouped


def match_comments_to_agents(
    agents_by_id: dict[str, dict],
    comments_by_name: dict[str, list[dict]],
) -> dict[str, list[dict]]:
    """에이전트 이름으로 댓글을 author_id에 매핑

    Returns:
        {author_id: [comment, ...]}
    """
    # author_name → author_id 역매핑
    name_to_id = {v["name"]: k for k, v in agents_by_id.items()}
    comments_by_id: dict[str, list[dict]] = defaultdict(list)

    for agent_name, comments in comments_by_name.items():
        if agent_name in name_to_id:
            aid = name_to_id[agent_name]
            comments_by_id[aid].extend(comments)
        else:
            # 이름이 posts에 없는 경우 — 별도 키로 보관
            comments_by_id[f"__unknown__{agent_name}"].extend(comments)

    return dict(comments_by_id)


# ──────────────────────────────────────────────
# 피처 추출
# ──────────────────────────────────────────────

def extract_post_features(posts: list[dict]) -> dict[str, Any]:
    """게시글 피처 추출"""
    if not posts:
        return {}

    lengths = [count_chars(p.get("content", "") + p.get("title", "")) for p in posts]
    honorific_flags = [has_honorific(p.get("content", "") + p.get("title", "")) for p in posts]
    question_counts = [count_question_marks(p.get("content", "") + p.get("title", "")) for p in posts]
    humor_counts = [count_humor_markers(p.get("content", "") + p.get("title", "")) for p in posts]
    helper_counts = [count_helper_markers(p.get("content", "") + p.get("title", "")) for p in posts]
    argumentative_flags = [detect_argumentative(p.get("content", "")) for p in posts]
    upvotes = [p.get("upvotes", 0) for p in posts]
    downvotes = [p.get("downvotes", 0) for p in posts]

    # 마당별 활동 분포
    submadang_counts: Counter = Counter(p.get("submadang", "unknown") for p in posts)
    total_posts = len(posts)
    submadang_ratio = {s: round(c / total_posts, 4) for s, c in submadang_counts.items()}

    # 활동 마당 범주 비율
    tech_ratio = sum(submadang_ratio.get(s, 0) for s in TECH_SUBMADANGS)
    social_ratio = sum(submadang_ratio.get(s, 0) for s in SOCIAL_SUBMADANGS)
    intel_ratio = sum(submadang_ratio.get(s, 0) for s in INTELLECTUAL_SUBMADANGS)
    finance_ratio = sum(submadang_ratio.get(s, 0) for s in FINANCE_SUBMADANGS)

    # 시간대별 활동
    hours = []
    for p in posts:
        ts = p.get("created_at", "")
        if ts:
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                hours.append(dt.hour)
            except ValueError:
                pass
    hour_dist = Counter(hours)
    peak_hour = max(hour_dist, key=hour_dist.get) if hour_dist else None

    return {
        "post_count": total_posts,
        "avg_length": round(safe_mean(lengths), 1),
        "length_stddev": round(stddev(lengths), 1),
        "avg_upvotes": round(safe_mean(upvotes), 3),
        "avg_downvotes": round(safe_mean(downvotes), 3),
        "honorific_ratio": round(sum(honorific_flags) / total_posts, 4),
        "avg_question_marks": round(safe_mean(question_counts), 3),
        "avg_humor_markers": round(safe_mean(humor_counts), 3),
        "avg_helper_markers": round(safe_mean(helper_counts), 3),
        "argumentative_ratio": round(sum(argumentative_flags) / total_posts, 4),
        "submadang_distribution": submadang_ratio,
        "unique_submadangs": len(submadang_counts),
        "top_submadang": submadang_counts.most_common(1)[0][0] if submadang_counts else None,
        "tech_ratio": round(tech_ratio, 4),
        "social_ratio": round(social_ratio, 4),
        "intellectual_ratio": round(intel_ratio, 4),
        "finance_ratio": round(finance_ratio, 4),
        "peak_hour": peak_hour,
        "hour_distribution": {str(h): c for h, c in sorted(hour_dist.items())},
    }


def extract_comment_features(comments: list[dict]) -> dict[str, Any]:
    """댓글 피처 추출"""
    if not comments:
        return {
            "comment_count": 0,
            "avg_comment_length": 0.0,
            "comment_honorific_ratio": 0.0,
            "comment_avg_question_marks": 0.0,
            "comment_avg_humor_markers": 0.0,
            "comment_avg_helper_markers": 0.0,
            "comment_argumentative_ratio": 0.0,
        }

    lengths = [count_chars(c.get("content", "")) for c in comments]
    honorific_flags = [has_honorific(c.get("content", "")) for c in comments]
    question_counts = [count_question_marks(c.get("content", "")) for c in comments]
    humor_counts = [count_humor_markers(c.get("content", "")) for c in comments]
    helper_counts = [count_helper_markers(c.get("content", "")) for c in comments]
    argumentative_flags = [detect_argumentative(c.get("content", "")) for c in comments]
    total = len(comments)

    return {
        "comment_count": total,
        "avg_comment_length": round(safe_mean(lengths), 1),
        "comment_honorific_ratio": round(sum(honorific_flags) / total, 4),
        "comment_avg_question_marks": round(safe_mean(question_counts), 3),
        "comment_avg_humor_markers": round(safe_mean(humor_counts), 3),
        "comment_avg_helper_markers": round(safe_mean(helper_counts), 3),
        "comment_argumentative_ratio": round(sum(argumentative_flags) / total, 4),
    }


# ──────────────────────────────────────────────
# 페르소나 분류 (규칙 기반)
# ──────────────────────────────────────────────

def score_personas(pf: dict[str, Any], cf: dict[str, Any]) -> dict[str, float]:
    """각 페르소나 유형별 점수 계산 (0~1 범위)

    게시글 피처(pf)와 댓글 피처(cf)를 결합하여 채점한다.
    """
    scores: dict[str, float] = {
        PERSONA_EXPERT: 0.0,
        PERSONA_FRIENDLY: 0.0,
        PERSONA_HUMOROUS: 0.0,
        PERSONA_SERIOUS: 0.0,
        PERSONA_CURIOUS: 0.0,
        PERSONA_HELPER: 0.0,
    }

    avg_len = pf.get("avg_length", 0)
    tech_ratio = pf.get("tech_ratio", 0)
    social_ratio = pf.get("social_ratio", 0)
    intel_ratio = pf.get("intellectual_ratio", 0)
    finance_ratio = pf.get("finance_ratio", 0)
    honorific_ratio = pf.get("honorific_ratio", 0)
    humor_markers = pf.get("avg_humor_markers", 0)
    question_marks = pf.get("avg_question_marks", 0)
    helper_markers = pf.get("avg_helper_markers", 0)
    argumentative_ratio = pf.get("argumentative_ratio", 0)
    unique_submadangs = pf.get("unique_submadangs", 1)
    length_stddev = pf.get("length_stddev", 0)

    # 댓글 피처 가중 결합
    c_honorific = cf.get("comment_honorific_ratio", 0)
    c_humor = cf.get("comment_avg_humor_markers", 0)
    c_question = cf.get("comment_avg_question_marks", 0)
    c_helper = cf.get("comment_avg_helper_markers", 0)
    c_argumentative = cf.get("comment_argumentative_ratio", 0)
    c_len = cf.get("avg_comment_length", 0)

    has_comments = cf.get("comment_count", 0) > 0
    w_p, w_c = (0.6, 0.4) if has_comments else (1.0, 0.0)

    # ── PER-EXPERT: 기술/전문 마당, 긴 글 ──
    expert_score = 0.0
    if tech_ratio > 0.5:
        expert_score += 0.35
    elif tech_ratio > 0.25:
        expert_score += 0.15
    if finance_ratio > 0.3:
        expert_score += 0.2
    if avg_len > 300:
        expert_score += 0.25
    elif avg_len > 150:
        expert_score += 0.1
    if argumentative_ratio > 0.4:
        expert_score += 0.15
    elif argumentative_ratio > 0.2:
        expert_score += 0.07
    scores[PERSONA_EXPERT] = min(1.0, expert_score * w_p + min(1.0, c_argumentative * 2) * 0.2 * w_c)

    # ── PER-FRIENDLY: 일상/대화체, 짧은 글, 존댓말 ──
    friendly_score = 0.0
    if social_ratio > 0.5:
        friendly_score += 0.35
    elif social_ratio > 0.2:
        friendly_score += 0.15
    if avg_len < 150:
        friendly_score += 0.2
    elif avg_len < 250:
        friendly_score += 0.1
    if honorific_ratio > 0.7:
        friendly_score += 0.2
    elif honorific_ratio > 0.4:
        friendly_score += 0.1
    if unique_submadangs >= 3:
        friendly_score += 0.1
    combined_honorific = honorific_ratio * w_p + c_honorific * w_c
    scores[PERSONA_FRIENDLY] = min(1.0, friendly_score + combined_honorific * 0.15)

    # ── PER-HUMOROUS: ㅋㅋ, ㅎㅎ, 이모지 빈도 ──
    combined_humor = humor_markers * w_p + c_humor * w_c
    humor_score = 0.0
    if combined_humor > 3:
        humor_score = 0.9
    elif combined_humor > 1.5:
        humor_score = 0.6
    elif combined_humor > 0.5:
        humor_score = 0.35
    elif combined_humor > 0.1:
        humor_score = 0.15
    scores[PERSONA_HUMOROUS] = min(1.0, humor_score)

    # ── PER-SERIOUS: 장문, 논증적, 낮은 유머 ──
    serious_score = 0.0
    if avg_len > 400:
        serious_score += 0.35
    elif avg_len > 250:
        serious_score += 0.2
    if argumentative_ratio > 0.5:
        serious_score += 0.3
    elif argumentative_ratio > 0.3:
        serious_score += 0.15
    if intel_ratio > 0.4:
        serious_score += 0.15
    if combined_humor < 0.3:
        serious_score += 0.1
    if honorific_ratio < 0.3:
        serious_score += 0.05
    scores[PERSONA_SERIOUS] = min(1.0, serious_score)

    # ── PER-CURIOUS: 물음표 비율 높음 ──
    combined_question = question_marks * w_p + c_question * w_c
    curious_score = 0.0
    if combined_question > 2:
        curious_score = 0.85
    elif combined_question > 1:
        curious_score = 0.65
    elif combined_question > 0.5:
        curious_score = 0.45
    elif combined_question > 0.2:
        curious_score = 0.25
    # 질문 마당 가산
    if pf.get("submadang_distribution", {}).get("questions", 0) > 0.1:
        curious_score += 0.1
    scores[PERSONA_CURIOUS] = min(1.0, curious_score)

    # ── PER-HELPER: 안내/설명/추천 패턴 ──
    combined_helper = helper_markers * w_p + c_helper * w_c
    helper_score = 0.0
    if combined_helper > 5:
        helper_score = 0.9
    elif combined_helper > 2.5:
        helper_score = 0.65
    elif combined_helper > 1:
        helper_score = 0.4
    elif combined_helper > 0.3:
        helper_score = 0.2
    scores[PERSONA_HELPER] = min(1.0, helper_score)

    return {k: round(v, 4) for k, v in scores.items()}


def classify_persona(scores: dict[str, float]) -> dict[str, Any]:
    """점수 기반 페르소나 유형 분류

    최고 점수 유형을 primary로, 0.3 이상인 나머지를 secondary로 분류한다.
    """
    if not scores:
        return {"primary": "PER-UNKNOWN", "secondary": [], "scores": {}}

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary = sorted_scores[0][0]
    primary_score = sorted_scores[0][1]

    # 점수가 0.1 미만이면 분류 불가
    if primary_score < 0.1:
        primary = "PER-UNKNOWN"

    secondary = [k for k, v in sorted_scores[1:] if v >= 0.3]

    return {
        "primary": primary,
        "primary_score": round(primary_score, 4),
        "secondary": secondary,
        "scores": scores,
    }


# ──────────────────────────────────────────────
# 프로필 카드 생성
# ──────────────────────────────────────────────

PERSONA_DESCRIPTIONS = {
    PERSONA_EXPERT: "전문가형 — 기술·전문 분야 중심, 심도 있는 내용 게시",
    PERSONA_FRIENDLY: "친근형 — 일상적 대화체, 따뜻한 소통 지향",
    PERSONA_HUMOROUS: "유머형 — 유머 표현 빈도 높음, 가벼운 분위기",
    PERSONA_SERIOUS: "진지형 — 장문 논증적 글, 심층 토론 선호",
    PERSONA_CURIOUS: "질문형 — 호기심 많음, 질문과 탐색을 통한 상호작용",
    PERSONA_HELPER: "도우미형 — 정보·서비스 안내, 독자 편의 중심",
    "PER-UNKNOWN": "미분류 — 데이터 부족으로 페르소나 판별 불가",
}


def build_profile_card(
    author_id: str,
    author_name: str,
    post_features: dict[str, Any],
    comment_features: dict[str, Any],
    persona: dict[str, Any],
    agent_summary: dict | None = None,
) -> dict[str, Any]:
    """에이전트 종합 프로필 카드 생성"""
    post_count = post_features.get("post_count", 0)
    comment_count = comment_features.get("comment_count", 0)
    total_activity = post_count + comment_count

    post_ratio = round(post_count / total_activity, 4) if total_activity > 0 else 0.0
    comment_ratio = round(comment_count / total_activity, 4) if total_activity > 0 else 0.0

    card: dict[str, Any] = {
        "author_id": author_id,
        "author_name": author_name,
        # ─── 활동 요약 ───
        "activity": {
            "post_count": post_count,
            "comment_count": comment_count,
            "post_ratio": post_ratio,
            "comment_ratio": comment_ratio,
            "avg_upvotes": post_features.get("avg_upvotes", 0),
            "avg_downvotes": post_features.get("avg_downvotes", 0),
            "peak_hour": post_features.get("peak_hour"),
            "hour_distribution": post_features.get("hour_distribution", {}),
        },
        # ─── 마당 분포 ───
        "submadang": {
            "distribution": post_features.get("submadang_distribution", {}),
            "unique_count": post_features.get("unique_submadangs", 0),
            "top_submadang": post_features.get("top_submadang"),
            "tech_ratio": post_features.get("tech_ratio", 0),
            "social_ratio": post_features.get("social_ratio", 0),
            "intellectual_ratio": post_features.get("intellectual_ratio", 0),
            "finance_ratio": post_features.get("finance_ratio", 0),
        },
        # ─── 문체 일관성 ───
        "style": {
            "avg_post_length": post_features.get("avg_length", 0),
            "post_length_stddev": post_features.get("length_stddev", 0),
            "avg_comment_length": comment_features.get("avg_comment_length", 0),
            "honorific_ratio": post_features.get("honorific_ratio", 0),
            "comment_honorific_ratio": comment_features.get("comment_honorific_ratio", 0),
            "avg_question_marks": post_features.get("avg_question_marks", 0),
            "avg_humor_markers": post_features.get("avg_humor_markers", 0),
            "argumentative_ratio": post_features.get("argumentative_ratio", 0),
            "avg_helper_markers": post_features.get("avg_helper_markers", 0),
        },
        # ─── 페르소나 ───
        "persona": {
            "primary": persona["primary"],
            "primary_score": persona["primary_score"],
            "secondary": persona["secondary"],
            "description": PERSONA_DESCRIPTIONS.get(persona["primary"], ""),
            "scores": persona["scores"],
        },
        # ─── 메타 ───
        "meta": {
            "analyzed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "data_source": "pilot_posts + agent_comments",
        },
    }

    # 요약 데이터에서 추가 정보 병합
    if agent_summary:
        card["activity"]["total_upvotes"] = agent_summary.get("total_upvotes", 0)
        card["activity"]["total_downvotes"] = agent_summary.get("total_downvotes", 0)
        card["activity"]["first_post"] = agent_summary.get("first_post")
        card["activity"]["last_post"] = agent_summary.get("last_post")

    return card


# ──────────────────────────────────────────────
# 인기-페르소나 상관 분석
# ──────────────────────────────────────────────

def analyze_popularity_correlation(profiles: list[dict]) -> dict[str, Any]:
    """페르소나 유형과 추천 수의 상관 분석

    각 페르소나 유형별 평균 추천 수와 에이전트 목록을 집계한다.
    """
    by_persona: dict[str, list[float]] = defaultdict(list)
    agent_persona_map: list[dict] = []

    for p in profiles:
        primary = p["persona"]["primary"]
        avg_up = p["activity"].get("avg_upvotes", 0)
        by_persona[primary].append(avg_up)
        agent_persona_map.append({
            "author_id": p["author_id"],
            "author_name": p["author_name"],
            "primary_persona": primary,
            "avg_upvotes": avg_up,
            "post_count": p["activity"]["post_count"],
        })

    persona_stats: dict[str, dict] = {}
    for persona, upvotes_list in by_persona.items():
        persona_stats[persona] = {
            "agent_count": len(upvotes_list),
            "avg_upvotes": round(safe_mean(upvotes_list), 3),
            "max_upvotes": round(max(upvotes_list), 3),
            "min_upvotes": round(min(upvotes_list), 3),
            "description": PERSONA_DESCRIPTIONS.get(persona, ""),
        }

    # 전체 순위 (평균 추천 수 기준)
    ranked = sorted(
        persona_stats.items(),
        key=lambda x: x[1]["avg_upvotes"],
        reverse=True,
    )
    ranked_list = [{"rank": i + 1, "persona": k, **v} for i, (k, v) in enumerate(ranked)]

    return {
        "persona_popularity_stats": persona_stats,
        "popularity_ranking": ranked_list,
        "agent_persona_upvotes": sorted(
            agent_persona_map, key=lambda x: x["avg_upvotes"], reverse=True
        ),
        "analyzed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


# ──────────────────────────────────────────────
# 메인 파이프라인
# ──────────────────────────────────────────────

def run_profiler(
    posts_path: str,
    raw_dir: str,
    summary_path: str,
    output_dir: str,
) -> None:
    """페르소나 프로파일링 전체 파이프라인 실행"""

    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)

    # ── 1. 데이터 로딩 ──
    logger.info("=== 1단계: 데이터 로딩 ===")
    posts = load_posts(posts_path)
    comments_by_name = load_comments(raw_dir)
    agent_summary_by_id = load_agent_summary(summary_path)

    # ── 2. 에이전트별 게시글 분류 ──
    logger.info("=== 2단계: 에이전트별 데이터 분류 ===")
    agents_posts = group_posts_by_agent(posts)
    comments_by_id = match_comments_to_agents(agents_posts, comments_by_name)

    logger.info(f"게시글 에이전트 수: {len(agents_posts)}")
    logger.info(f"댓글 보유 에이전트 수: {len(comments_by_id)}")

    # ── 3. 피처 추출 & 프로필 카드 생성 ──
    logger.info("=== 3단계: 피처 추출 및 페르소나 분류 ===")
    profiles: list[dict] = []

    for author_id, agent_data in agents_posts.items():
        author_name = agent_data["name"]
        agent_posts = agent_data["posts"]
        agent_comments = comments_by_id.get(author_id, [])
        agent_summary = agent_summary_by_id.get(author_id)

        # 피처 추출
        pf = extract_post_features(agent_posts)
        cf = extract_comment_features(agent_comments)

        # 페르소나 분류
        scores = score_personas(pf, cf)
        persona = classify_persona(scores)

        # 프로필 카드 생성
        card = build_profile_card(
            author_id=author_id,
            author_name=author_name,
            post_features=pf,
            comment_features=cf,
            persona=persona,
            agent_summary=agent_summary,
        )
        profiles.append(card)

        logger.info(
            f"  {author_name:25s} | 게시글 {len(agent_posts):3d}개 "
            f"| 댓글 {len(agent_comments):3d}개 "
            f"| 페르소나: {persona['primary']} ({persona['primary_score']:.2f})"
        )

    # 게시글 수 기준 내림차순 정렬
    profiles.sort(key=lambda x: x["activity"]["post_count"], reverse=True)

    # ── 4. 페르소나 유형별 요약 ──
    logger.info("=== 4단계: 페르소나 유형 요약 ===")
    persona_types: dict[str, dict] = {}
    for card in profiles:
        ptype = card["persona"]["primary"]
        if ptype not in persona_types:
            persona_types[ptype] = {
                "type": ptype,
                "description": PERSONA_DESCRIPTIONS.get(ptype, ""),
                "agents": [],
                "count": 0,
            }
        persona_types[ptype]["agents"].append({
            "author_id": card["author_id"],
            "author_name": card["author_name"],
            "primary_score": card["persona"]["primary_score"],
            "post_count": card["activity"]["post_count"],
            "avg_upvotes": card["activity"]["avg_upvotes"],
        })
        persona_types[ptype]["count"] += 1

    # 유형 내 에이전트를 게시글 수 기준 정렬
    for ptype in persona_types.values():
        ptype["agents"].sort(key=lambda x: x["post_count"], reverse=True)

    persona_types_output = {
        "summary": {
            k: {"count": v["count"], "description": v["description"]}
            for k, v in persona_types.items()
        },
        "types": persona_types,
        "analyzed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    # ── 5. 인기-페르소나 상관 분석 ──
    logger.info("=== 5단계: 인기-페르소나 상관 분석 ===")
    popularity_corr = analyze_popularity_correlation(profiles)

    # ── 6. 결과 저장 ──
    logger.info("=== 6단계: 결과 저장 ===")

    profiles_path = os.path.join(output_dir, "agent_profiles.json")
    with open(profiles_path, "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=2)
    logger.info(f"에이전트 프로필 저장: {profiles_path} ({len(profiles)}개)")

    persona_path = os.path.join(output_dir, "persona_types.json")
    with open(persona_path, "w", encoding="utf-8") as f:
        json.dump(persona_types_output, f, ensure_ascii=False, indent=2)
    logger.info(f"페르소나 유형 저장: {persona_path}")

    popularity_path = os.path.join(output_dir, "popularity_correlation.json")
    with open(popularity_path, "w", encoding="utf-8") as f:
        json.dump(popularity_corr, f, ensure_ascii=False, indent=2)
    logger.info(f"인기-페르소나 상관 저장: {popularity_path}")

    # ── 7. 콘솔 요약 출력 ──
    logger.info("")
    logger.info("=== 분석 완료 요약 ===")
    logger.info(f"분석 에이전트 수: {len(profiles)}")
    logger.info("페르소나 유형 분포:")
    for ptype, data in sorted(persona_types.items(), key=lambda x: x[1]["count"], reverse=True):
        logger.info(f"  {ptype:20s}: {data['count']:3d}명 — {data['description']}")

    logger.info("\n인기도 순위 (페르소나별 평균 추천 수):")
    for item in popularity_corr["popularity_ranking"]:
        logger.info(
            f"  {item['rank']}위 {item['persona']:20s}: "
            f"평균 {item['avg_upvotes']:.2f}추천 / {item['agent_count']}에이전트"
        )


# ──────────────────────────────────────────────
# CLI 진입점
# ──────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="봇마당 에이전트 페르소나 프로파일러",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python scripts/profiler.py
  python scripts/profiler.py --output analysis/profiles/
  python scripts/profiler.py --posts data/raw/pilot_posts.json --raw-dir data/raw/
        """,
    )
    parser.add_argument(
        "--posts",
        default=os.path.join(RAW_DATA_DIR, "pilot_posts.json"),
        help="게시글 JSON 파일 경로 (기본값: data/raw/pilot_posts.json)",
    )
    parser.add_argument(
        "--raw-dir",
        default=RAW_DATA_DIR,
        help="에이전트 댓글 파일이 있는 디렉토리 (기본값: data/raw/)",
    )
    parser.add_argument(
        "--summary",
        default=os.path.join(PROCESSED_DATA_DIR, "agent_summary.json"),
        help="에이전트 요약 JSON 파일 경로 (기본값: data/processed/agent_summary.json)",
    )
    parser.add_argument(
        "--output",
        default=ANALYSIS_PROFILES_DIR,
        help="출력 디렉토리 (기본값: analysis/profiles/)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_profiler(
        posts_path=args.posts,
        raw_dir=args.raw_dir,
        summary_path=args.summary,
        output_dir=args.output,
    )


if __name__ == "__main__":
    main()
