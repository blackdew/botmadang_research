#!/usr/bin/env python3
"""봇마당 2주 종단 데이터 수집 및 시간 패턴 분석

Gen-4 이슈 #58: 시간 범위 확장 — 2주 종단 수집
기존 스냅샷 수집의 한계를 보완하여 시간에 따른 변화 패턴을 포착한다.

사용법:
    python scripts/collect_longitudinal.py
"""

import json
import logging
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.collector import BotmadangCollector, save_json
from scripts.config import RAW_DATA_DIR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# 프로젝트 루트
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def parse_datetime(dt_str: str) -> datetime | None:
    """ISO 형식 날짜 문자열을 datetime으로 변환"""
    if not dt_str:
        return None
    try:
        # 다양한 ISO 포맷 처리
        dt_str = dt_str.replace("Z", "+00:00")
        return datetime.fromisoformat(dt_str)
    except ValueError:
        try:
            return datetime.strptime(dt_str[:19], "%Y-%m-%dT%H:%M:%S").replace(
                tzinfo=timezone.utc
            )
        except ValueError:
            return None


def collect_2weeks_posts(collector: BotmadangCollector) -> list[dict]:
    """최근 2주간 게시글을 시간순으로 수집

    newest 정렬로 수집하면서 2주 경계에 도달하면 수집을 중단한다.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=14)
    logger.info(f"2주 종단 수집 시작 (기준: {cutoff.isoformat()[:10]} 이후)")

    all_posts = []
    cursor = None
    page_size = 100
    pages = 0

    while True:
        params = {"limit": page_size, "sort": "newest"}
        if cursor:
            params["cursor"] = cursor

        data = collector._get("/posts", params)
        if not data.get("success", True) or "posts" not in data:
            logger.error(f"수집 실패: {data.get('error', 'unknown')}")
            break

        posts = data["posts"]
        if not posts:
            logger.info("더 이상 게시글이 없음")
            break

        pages += 1

        # 2주 경계 체크
        reached_cutoff = False
        for post in posts:
            dt = parse_datetime(post.get("created_at", ""))
            if dt and dt < cutoff:
                reached_cutoff = True
                break
            all_posts.append(post)

        logger.info(f"  페이지 {pages}: 누적 {len(all_posts)}개 수집")

        if reached_cutoff:
            logger.info(f"  2주 경계 도달, 수집 종료")
            break

        if not data.get("has_more"):
            logger.info("  마지막 페이지 도달")
            break

        cursor = data.get("next_cursor")

    logger.info(f"총 {len(all_posts)}개 게시글 수집 완료 (API 요청 {pages}회)")
    return all_posts


def analyze_temporal_patterns(posts: list[dict]) -> dict:
    """시간 패턴 분석: 일별/시간대별 활동, 에이전트 등장 패턴"""

    # 일별 집계
    daily_posts = defaultdict(list)
    daily_agents = defaultdict(set)
    hourly_counts = Counter()
    agent_daily_activity = defaultdict(lambda: defaultdict(int))
    submadang_daily = defaultdict(lambda: defaultdict(int))

    for post in posts:
        dt = parse_datetime(post.get("created_at", ""))
        if not dt:
            continue

        date_str = dt.strftime("%Y-%m-%d")
        hour = dt.hour
        agent_name = post.get("author_name", "unknown")
        agent_id = post.get("author_id", "unknown")
        submadang = post.get("submadang", "unknown")

        daily_posts[date_str].append(post)
        daily_agents[date_str].add(agent_id)
        hourly_counts[hour] += 1
        agent_daily_activity[agent_name][date_str] += 1
        submadang_daily[submadang][date_str] += 1

    # 날짜 정렬
    sorted_dates = sorted(daily_posts.keys())

    # 일별 요약
    daily_summary = []
    for date in sorted_dates:
        day_posts = daily_posts[date]
        agents = daily_agents[date]
        upvotes = sum(p.get("upvotes", 0) for p in day_posts)
        comments = sum(p.get("comment_count", 0) for p in day_posts)
        top_agents = Counter(
            p.get("author_name", "unknown") for p in day_posts
        ).most_common(5)

        daily_summary.append({
            "date": date,
            "weekday": datetime.strptime(date, "%Y-%m-%d").strftime("%A"),
            "post_count": len(day_posts),
            "active_agents": len(agents),
            "total_upvotes": upvotes,
            "total_comments": comments,
            "top_agents": [
                {"name": name, "posts": count} for name, count in top_agents
            ],
        })

    # 시간대별 요약 (0~23시)
    hourly_summary = []
    for hour in range(24):
        hourly_summary.append({
            "hour": hour,
            "label": f"{hour:02d}:00-{hour:02d}:59",
            "post_count": hourly_counts.get(hour, 0),
        })

    # 에이전트별 활동 일수 및 패턴
    agent_patterns = []
    for agent_name, daily in agent_daily_activity.items():
        active_days = len(daily)
        total_posts = sum(daily.values())
        first_day = min(daily.keys())
        last_day = max(daily.keys())
        agent_patterns.append({
            "agent_name": agent_name,
            "active_days": active_days,
            "total_posts": total_posts,
            "avg_posts_per_active_day": round(total_posts / active_days, 2),
            "first_active": first_day,
            "last_active": last_day,
            "daily_breakdown": dict(sorted(daily.items())),
        })
    agent_patterns.sort(key=lambda x: x["total_posts"], reverse=True)

    # 마당별 일별 트렌드
    submadang_trends = {}
    for submadang, daily in submadang_daily.items():
        submadang_trends[submadang] = {
            "total_posts": sum(daily.values()),
            "active_days": len(daily),
            "daily": dict(sorted(daily.items())),
        }

    # 전체 통계
    all_dates = sorted_dates
    total_days = len(all_dates)
    total_posts_count = len(posts)
    all_agents = set()
    for agents in daily_agents.values():
        all_agents.update(agents)

    stats = {
        "period": {
            "start": all_dates[0] if all_dates else None,
            "end": all_dates[-1] if all_dates else None,
            "total_days": total_days,
        },
        "totals": {
            "posts": total_posts_count,
            "unique_agents": len(all_agents),
            "avg_posts_per_day": round(total_posts_count / total_days, 2)
            if total_days > 0
            else 0,
            "avg_agents_per_day": round(
                sum(len(a) for a in daily_agents.values()) / total_days, 2
            )
            if total_days > 0
            else 0,
        },
        "peak_day": max(daily_summary, key=lambda x: x["post_count"])
        if daily_summary
        else None,
        "quietest_day": min(daily_summary, key=lambda x: x["post_count"])
        if daily_summary
        else None,
        "peak_hour": max(hourly_summary, key=lambda x: x["post_count"])["hour"]
        if hourly_summary
        else None,
    }

    return {
        "collection_timestamp": datetime.now(timezone.utc).isoformat(),
        "statistics": stats,
        "daily_summary": daily_summary,
        "hourly_summary": hourly_summary,
        "agent_patterns": agent_patterns[:50],  # 상위 50명
        "submadang_trends": submadang_trends,
    }


def generate_analysis_report(analysis: dict, posts: list[dict]) -> str:
    """분석 결과를 마크다운 보고서로 생성"""
    stats = analysis["statistics"]
    daily = analysis["daily_summary"]
    hourly = analysis["hourly_summary"]
    agents = analysis["agent_patterns"]
    submadangs = analysis["submadang_trends"]

    period = stats["period"]
    totals = stats["totals"]

    lines = [
        "# Gen-4 종단 분석: 2주 시간 패턴",
        "",
        f"**수집일시**: {analysis['collection_timestamp'][:19]}",
        f"**분석 기간**: {period['start']} ~ {period['end']} ({period['total_days']}일)",
        f"**총 게시글**: {totals['posts']}개 / **고유 에이전트**: {totals['unique_agents']}명",
        "",
        "---",
        "",
        "## 1. 일별 활동 추이",
        "",
        "| 날짜 | 요일 | 게시글 | 활동 에이전트 | 추천 | 댓글 |",
        "|------|------|--------|---------------|------|------|",
    ]

    for d in daily:
        lines.append(
            f"| {d['date']} | {d['weekday'][:3]} | {d['post_count']} | "
            f"{d['active_agents']} | {d['total_upvotes']} | {d['total_comments']} |"
        )

    # 일별 트렌드 요약
    if daily:
        post_counts = [d["post_count"] for d in daily]
        agent_counts = [d["active_agents"] for d in daily]
        lines.extend([
            "",
            f"- 일평균 게시글: **{totals['avg_posts_per_day']}개**",
            f"- 일평균 활동 에이전트: **{totals['avg_agents_per_day']}명**",
            f"- 최고 활동일: **{stats['peak_day']['date']}** ({stats['peak_day']['post_count']}개)",
            f"- 최저 활동일: **{stats['quietest_day']['date']}** ({stats['quietest_day']['post_count']}개)",
            f"- 게시글 수 범위: {min(post_counts)} ~ {max(post_counts)}개",
        ])

    # 시간대별 분석
    lines.extend([
        "",
        "## 2. 시간대별 활동 패턴 (UTC)",
        "",
        "| 시간대 | 게시글 수 | 비율 |",
        "|--------|----------|------|",
    ])

    total_h = sum(h["post_count"] for h in hourly)
    for h in hourly:
        pct = round(h["post_count"] / total_h * 100, 1) if total_h > 0 else 0
        bar = "#" * int(pct / 2)
        lines.append(f"| {h['label']} | {h['post_count']} | {pct}% {bar} |")

    if stats.get("peak_hour") is not None:
        lines.extend([
            "",
            f"- 최고 활동 시간대: **{stats['peak_hour']:02d}:00 UTC**",
            "- AI 에이전트는 24시간 활동하므로 인간 사용자와 다른 패턴 예상",
        ])

    # 에이전트 활동 패턴
    lines.extend([
        "",
        "## 3. 에이전트 활동 패턴 (상위 20)",
        "",
        "| 에이전트 | 총 게시글 | 활동 일수 | 일평균 | 첫 활동 | 마지막 활동 |",
        "|----------|----------|----------|--------|---------|------------|",
    ])

    for a in agents[:20]:
        lines.append(
            f"| {a['agent_name']} | {a['total_posts']} | {a['active_days']}일 | "
            f"{a['avg_posts_per_active_day']} | {a['first_active']} | {a['last_active']} |"
        )

    # 에이전트 유형 분류
    if agents:
        persistent = [a for a in agents if a["active_days"] >= 7]
        sporadic = [a for a in agents if 2 <= a["active_days"] < 7]
        oneshot = [a for a in agents if a["active_days"] == 1]
        lines.extend([
            "",
            "### 활동 유형 분류",
            f"- **지속형** (7일+ 활동): {len(persistent)}명",
            f"- **간헐형** (2~6일 활동): {len(sporadic)}명",
            f"- **일회형** (1일만 활동): {len(oneshot)}명",
        ])
        if persistent:
            lines.append(f"- 지속형 에이전트: {', '.join(a['agent_name'] for a in persistent[:10])}")

    # 마당별 트렌드
    lines.extend([
        "",
        "## 4. 마당(서브마당)별 트렌드",
        "",
        "| 마당 | 총 게시글 | 활동 일수 |",
        "|------|----------|----------|",
    ])

    sorted_submadangs = sorted(
        submadangs.items(), key=lambda x: x[1]["total_posts"], reverse=True
    )
    for name, data in sorted_submadangs:
        lines.append(f"| {name} | {data['total_posts']} | {data['active_days']}일 |")

    # 연구 함의
    lines.extend([
        "",
        "## 5. 연구 함의 (Gen-4 기여)",
        "",
        "### 기존 발견과의 연결",
        "",
        "- **F1(다층적 정체성)**: 에이전트별 활동 패턴(지속/간헐/일회)이 페르소나 유지 전략과 연결",
        "- **F2(자기 참조 담화)**: 지속형 에이전트의 시간에 따른 담화 변화 추적 가능",
        "- **F5(규범 형성)**: 시간대별 활동 패턴이 커뮤니티 리듬을 형성하는지 확인",
        "",
        "### 새로운 관찰",
        "",
    ])

    if daily:
        # 활동량 변화 트렌드
        first_half = daily[:len(daily)//2]
        second_half = daily[len(daily)//2:]
        if first_half and second_half:
            avg_first = sum(d["post_count"] for d in first_half) / len(first_half)
            avg_second = sum(d["post_count"] for d in second_half) / len(second_half)
            trend = "증가" if avg_second > avg_first else "감소" if avg_second < avg_first else "유지"
            lines.append(
                f"- 2주간 활동량 {trend} 추세 "
                f"(전반 평균 {avg_first:.1f} → 후반 평균 {avg_second:.1f})"
            )

        # 요일 패턴
        weekday_counts = defaultdict(list)
        for d in daily:
            weekday_counts[d["weekday"]].append(d["post_count"])
        weekday_avg = {
            wd: round(sum(counts) / len(counts), 1)
            for wd, counts in weekday_counts.items()
        }
        if weekday_avg:
            busiest = max(weekday_avg, key=weekday_avg.get)
            quietest = min(weekday_avg, key=weekday_avg.get)
            lines.append(f"- 요일별 패턴: {busiest}가 가장 활발 ({weekday_avg[busiest]}), "
                        f"{quietest}가 가장 조용 ({weekday_avg[quietest]})")

    lines.extend([
        "",
        "### 포화도 기여 예상",
        "",
        "- 시간 차원 추가로 코드 포화 강화 (시간 관련 코드 추가 가능)",
        "- 에이전트 활동 패턴이 페르소나 분석의 새로운 축 제공",
        "- 종단 데이터로 주제 안정성 검증 강화",
        "",
        "---",
        "",
        f"*Gen-4 종단 분석 완료 — {analysis['collection_timestamp'][:10]}*",
    ])

    return "\n".join(lines)


def main():
    """2주 종단 수집 및 분석 실행"""
    logger.info("=" * 60)
    logger.info("Gen-4 종단 수집 시작: 2주 시간 범위 확장")
    logger.info("=" * 60)

    # API 키 로드
    api_key = os.environ.get("BOTMADANG_API_KEY")
    if not api_key:
        env_path = os.path.join(PROJECT_ROOT, ".env")
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("BOTMADANG_API_KEY="):
                        api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                        break

    collector = BotmadangCollector(api_key=api_key)

    # 1. 2주 데이터 수집
    posts = collect_2weeks_posts(collector)
    if not posts:
        logger.error("게시글 수집 실패")
        sys.exit(1)

    # 수집 데이터 저장
    output_path = os.path.join(RAW_DATA_DIR, "longitudinal_2weeks.json")
    save_json(posts, output_path)
    logger.info(f"종단 데이터 저장: {output_path} ({len(posts)}개)")

    # 2. 시간 패턴 분석
    logger.info("시간 패턴 분석 시작...")
    analysis = analyze_temporal_patterns(posts)

    # 분석 결과 JSON 저장
    analysis_json_path = os.path.join(
        PROJECT_ROOT, "analysis", "evolution", "gen-4_longitudinal_data.json"
    )
    save_json(analysis, analysis_json_path)

    # 3. 분석 보고서 생성
    report = generate_analysis_report(analysis, posts)
    report_path = os.path.join(
        PROJECT_ROOT, "analysis", "evolution", "gen-4_longitudinal_analysis.md"
    )
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    logger.info(f"분석 보고서 저장: {report_path}")

    # 요약 출력
    stats = analysis["statistics"]
    print("\n" + "=" * 60)
    print("Gen-4 종단 수집·분석 완료")
    print("=" * 60)
    print(f"  기간: {stats['period']['start']} ~ {stats['period']['end']}")
    print(f"  일수: {stats['period']['total_days']}일")
    print(f"  게시글: {stats['totals']['posts']}개")
    print(f"  에이전트: {stats['totals']['unique_agents']}명")
    print(f"  일평균: {stats['totals']['avg_posts_per_day']}개/일")
    print(f"  데이터: {output_path}")
    print(f"  보고서: {report_path}")
    print(f"  API 요청: {collector._request_count}회")


if __name__ == "__main__":
    main()
