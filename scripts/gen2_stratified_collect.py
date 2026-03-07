#!/usr/bin/env python3
"""Gen-2 균등 샘플링: 에이전트별 최대 30개 게시글 수집

Gen-1의 방법론적 반론(상위 3명 61% 독점)을 해소하기 위해,
에이전트별 균등 할당 샘플링을 수행한다.

사용법:
    python scripts/gen2_stratified_collect.py
"""

import json
import logging
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.collector import BotmadangCollector, save_json
from scripts.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

AGENT_LIMIT_PER_AGENT = 30


def load_agent_summary(filepath: str) -> list[dict]:
    """agent_summary.json에서 에이전트 목록을 로드한다."""
    with open(filepath, "r", encoding="utf-8") as f:
        agents = json.load(f)
    logger.info(f"에이전트 목록 로드: {len(agents)}명")
    return agents


def collect_all_agents(
    collector: BotmadangCollector,
    agents: list[dict],
    limit_per_agent: int = AGENT_LIMIT_PER_AGENT,
) -> tuple[list[dict], list[dict]]:
    """모든 에이전트의 게시글을 수집한다.

    Returns:
        (all_posts, sampling_report)
    """
    all_posts = []
    sampling_report = []

    for i, agent in enumerate(agents):
        agent_id = agent["author_id"]
        agent_name = agent["author_name"]
        gen1_count = agent["post_count"]

        logger.info(
            f"[{i+1}/{len(agents)}] {agent_name} (Gen-1: {gen1_count}개) 수집 중..."
        )

        posts = collector.collect_agent_posts(agent_id, limit=limit_per_agent)

        # 에이전트 이름 필드 보완 (API 응답에 없을 경우 대비)
        for post in posts:
            if not post.get("author_name"):
                post["author_name"] = agent_name
            if not post.get("author_id"):
                post["author_id"] = agent_id

        collected_count = len(posts)
        all_posts.extend(posts)

        report_entry = {
            "author_id": agent_id,
            "author_name": agent_name,
            "gen1_post_count": gen1_count,
            "gen2_collected": collected_count,
            "target": limit_per_agent,
            "achieved_target": collected_count >= limit_per_agent,
        }
        sampling_report.append(report_entry)

        logger.info(f"  -> {collected_count}개 수집 (목표: {limit_per_agent}개)")

    return all_posts, sampling_report


def compute_basic_stats(
    all_posts: list[dict], sampling_report: list[dict]
) -> dict:
    """기초 통계를 계산한다."""
    total_collected = len(all_posts)

    # 에이전트별 실제 수집 수
    agent_counts = {r["author_name"]: r["gen2_collected"] for r in sampling_report}

    # 마당별 분포
    madang_counts: dict[str, int] = {}
    for post in all_posts:
        madang = post.get("submadang", "unknown")
        madang_counts[madang] = madang_counts.get(madang, 0) + 1

    # general 마당 비율
    general_count = madang_counts.get("general", 0)
    general_ratio = round(general_count / total_collected, 4) if total_collected > 0 else 0.0

    # 글 길이 통계
    lengths = [len(post.get("content", "")) for post in all_posts]
    avg_length = round(sum(lengths) / len(lengths), 1) if lengths else 0.0

    # 댓글 수 분포
    comment_counts = [post.get("comment_count", 0) for post in all_posts]
    avg_comments = (
        round(sum(comment_counts) / len(comment_counts), 2) if comment_counts else 0.0
    )

    # 에이전트 집중도: 상위 3명이 차지하는 비율
    sorted_agents = sorted(agent_counts.items(), key=lambda x: x[1], reverse=True)
    top3_count = sum(c for _, c in sorted_agents[:3])
    top3_ratio = round(top3_count / total_collected, 4) if total_collected > 0 else 0.0

    stats = {
        "total_collected": total_collected,
        "agent_count": len(sampling_report),
        "avg_post_length": avg_length,
        "avg_comments_per_post": avg_comments,
        "madang_distribution": dict(
            sorted(madang_counts.items(), key=lambda x: x[1], reverse=True)
        ),
        "general_ratio": general_ratio,
        "general_ratio_target": "< 0.40",
        "general_ratio_ok": general_ratio < 0.40,
        "top3_agents": [{"name": n, "count": c} for n, c in sorted_agents[:3]],
        "top3_concentration": top3_ratio,
        "agent_distribution": dict(sorted_agents),
    }
    return stats


def main():
    logger.info("=" * 60)
    logger.info("Gen-2 균등 샘플링 수집 시작")
    logger.info(f"에이전트별 목표: {AGENT_LIMIT_PER_AGENT}개")
    logger.info("=" * 60)

    # 1단계: 에이전트 목록 로드
    agent_summary_path = os.path.join(PROCESSED_DATA_DIR, "agent_summary.json")
    if not os.path.exists(agent_summary_path):
        logger.error(f"agent_summary.json 없음: {agent_summary_path}")
        sys.exit(1)

    agents = load_agent_summary(agent_summary_path)

    # 2단계: 수집기 초기화
    api_key = os.environ.get("BOTMADANG_API_KEY")
    collector = BotmadangCollector(api_key=api_key)

    # 3단계: 에이전트별 게시글 수집
    logger.info(f"\n[수집 시작] {len(agents)}명 에이전트, 에이전트당 최대 {AGENT_LIMIT_PER_AGENT}개")
    all_posts, sampling_report = collect_all_agents(
        collector, agents, limit_per_agent=AGENT_LIMIT_PER_AGENT
    )

    logger.info(f"\n총 수집: {len(all_posts)}개 게시글")

    # 4단계: 중복 제거 (post_id 기준)
    seen_ids: set[str] = set()
    deduplicated: list[dict] = []
    duplicates = 0
    for post in all_posts:
        pid = post.get("id") or post.get("post_id")
        if pid and pid in seen_ids:
            duplicates += 1
        else:
            if pid:
                seen_ids.add(pid)
            deduplicated.append(post)

    logger.info(f"중복 제거: {duplicates}건 제거, {len(deduplicated)}건 유지")

    # 5단계: 기초 통계 계산
    stats = compute_basic_stats(deduplicated, sampling_report)

    # 6단계: 저장
    output_posts_path = os.path.join(RAW_DATA_DIR, "gen2_stratified_posts.json")
    save_json(deduplicated, output_posts_path)

    # 샘플링 리포트에 메타데이터 추가
    report_output = {
        "timestamp": datetime.now().astimezone().isoformat(),
        "collection_params": {
            "limit_per_agent": AGENT_LIMIT_PER_AGENT,
            "total_agents": len(agents),
        },
        "data_quality": {
            "total_before_dedup": len(all_posts),
            "duplicates_removed": duplicates,
            "total_after_dedup": len(deduplicated),
            "missing_content": sum(1 for p in deduplicated if not p.get("content")),
        },
        "basic_stats": stats,
        "agent_sampling": sampling_report,
        "total_api_requests": collector._request_count,
    }
    report_path = os.path.join(PROCESSED_DATA_DIR, "gen2_sampling_report.json")
    save_json(report_output, report_path)

    # 7단계: 결과 출력
    logger.info("\n" + "=" * 60)
    logger.info("Gen-2 균등 샘플링 수집 완료")
    logger.info("=" * 60)
    logger.info(f"저장: {output_posts_path}")
    logger.info(f"리포트: {report_path}")
    logger.info(f"총 API 요청: {collector._request_count}회")
    logger.info("")
    logger.info("[수집 결과 요약]")
    logger.info(f"  총 게시글: {len(deduplicated)}건")
    logger.info(f"  에이전트 수: {len(sampling_report)}명")
    logger.info(f"  중복 제거: {duplicates}건")
    logger.info(f"  평균 글 길이: {stats['avg_post_length']}자")
    logger.info(f"  평균 댓글 수: {stats['avg_comments_per_post']}개")
    logger.info("")
    logger.info("[마당별 분포]")
    for madang, count in stats["madang_distribution"].items():
        pct = round(count / len(deduplicated) * 100, 1) if deduplicated else 0
        logger.info(f"  {madang}: {count}건 ({pct}%)")
    logger.info("")
    logger.info(f"  general 비율: {stats['general_ratio']*100:.1f}% (목표: < 40%)")
    status = "달성" if stats["general_ratio_ok"] else "미달성"
    logger.info(f"  general 비율 목표: {status}")
    logger.info("")
    logger.info("[에이전트 상위 3명]")
    for entry in stats["top3_agents"]:
        pct = round(entry["count"] / len(deduplicated) * 100, 1) if deduplicated else 0
        logger.info(f"  {entry['name']}: {entry['count']}건 ({pct}%)")
    logger.info(
        f"  상위 3명 집중도: {stats['top3_concentration']*100:.1f}% "
        f"(Gen-1: 61%)"
    )

    return report_output


if __name__ == "__main__":
    main()
