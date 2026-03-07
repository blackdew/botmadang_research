#!/usr/bin/env python3
"""봇마당 API 데이터 수집기

봇마당(botmadang.org) REST API에서 게시글, 에이전트 정보를 수집한다.
Rate limit(분당 100회)을 준수하며, cursor 기반 페이지네이션을 지원한다.

사용법:
    python scripts/collector.py posts --limit 500
    python scripts/collector.py posts --submadang general --limit 200
    python scripts/collector.py agent-posts --agent-id <id> --limit 100
    python scripts/collector.py stats
    python scripts/collector.py pilot
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

# 프로젝트 루트를 path에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.config import (
    API_BASE_URL,
    DEFAULT_PAGE_SIZE,
    MAX_RETRIES,
    PROCESSED_DATA_DIR,
    RAW_DATA_DIR,
    REQUEST_INTERVAL,
    RETRY_DELAY,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


class BotmadangCollector:
    """봇마당 API 데이터 수집기"""

    def __init__(self, api_key: str | None = None):
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
        self._last_request_time = 0.0
        self._request_count = 0

    def _rate_limit(self):
        """Rate limit 준수: 분당 100회"""
        elapsed = time.time() - self._last_request_time
        if elapsed < REQUEST_INTERVAL:
            time.sleep(REQUEST_INTERVAL - elapsed)
        self._last_request_time = time.time()
        self._request_count += 1

    def _get(self, endpoint: str, params: dict | None = None) -> dict:
        """API GET 요청 (재시도 로직 포함)"""
        url = f"{API_BASE_URL}{endpoint}"
        for attempt in range(MAX_RETRIES):
            self._rate_limit()
            try:
                resp = self.session.get(url, params=params, timeout=30)
                if resp.status_code == 200:
                    return resp.json()
                elif resp.status_code == 429:
                    wait = RETRY_DELAY * (attempt + 1)
                    logger.warning(f"Rate limited, waiting {wait}s...")
                    time.sleep(wait)
                    continue
                elif resp.status_code == 401:
                    logger.error(f"인증 필요: {endpoint}")
                    return {"success": False, "error": "auth_required"}
                else:
                    logger.warning(f"HTTP {resp.status_code}: {endpoint} (attempt {attempt+1})")
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(RETRY_DELAY)
            except requests.RequestException as e:
                logger.warning(f"요청 실패: {e} (attempt {attempt+1})")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
        logger.error(f"최대 재시도 초과: {endpoint}")
        return {"success": False, "error": "max_retries_exceeded"}

    def collect_posts(
        self,
        limit: int = 500,
        submadang: str | None = None,
        sort: str | None = None,
    ) -> list[dict]:
        """게시글 수집 (cursor 페이지네이션)"""
        all_posts = []
        cursor = None
        page_size = min(limit, DEFAULT_PAGE_SIZE)

        logger.info(f"게시글 수집 시작 (목표: {limit}개, 마당: {submadang or '전체'})")

        while len(all_posts) < limit:
            params = {"limit": page_size}
            if cursor:
                params["cursor"] = cursor
            if submadang:
                params["submadang"] = submadang
            if sort:
                params["sort"] = sort

            data = self._get("/posts", params)
            if not data.get("success", True) or "posts" not in data:
                logger.error(f"게시글 수집 실패: {data.get('error', 'unknown')}")
                break

            posts = data["posts"]
            if not posts:
                logger.info("더 이상 게시글이 없음")
                break

            all_posts.extend(posts)
            logger.info(f"  수집: {len(all_posts)}/{limit}개")

            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")

        return all_posts[:limit]

    def collect_agent_posts(self, agent_id: str, limit: int = 100) -> list[dict]:
        """특정 에이전트의 게시글 수집"""
        all_posts = []
        cursor = None

        logger.info(f"에이전트 {agent_id} 게시글 수집 (목표: {limit}개)")

        while len(all_posts) < limit:
            params = {}
            if cursor:
                params["cursor"] = cursor

            data = self._get(f"/agents/{agent_id}/posts", params)
            if "posts" not in data:
                break

            posts = data["posts"]
            if not posts:
                break

            all_posts.extend(posts)
            logger.info(f"  수집: {len(all_posts)}개")

            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")

        return all_posts[:limit]

    def collect_agent_comments(self, agent_id: str, limit: int = 100) -> list[dict]:
        """특정 에이전트의 댓글 수집"""
        all_comments = []
        cursor = None

        logger.info(f"에이전트 {agent_id} 댓글 수집 (목표: {limit}개)")

        while len(all_comments) < limit:
            params = {}
            if cursor:
                params["cursor"] = cursor

            data = self._get(f"/agents/{agent_id}/comments", params)
            if "comments" not in data:
                break

            comments = data["comments"]
            if not comments:
                break

            all_comments.extend(comments)
            logger.info(f"  수집: {len(all_comments)}개")

            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")

        return all_comments[:limit]

    def collect_stats(self) -> dict:
        """플랫폼 통계 수집"""
        logger.info("플랫폼 통계 수집")
        return self._get("/stats")

    def collect_pilot(self, post_limit: int = 500) -> dict:
        """파일럿 데이터 수집: 게시글 + 통계 + 에이전트 요약"""
        logger.info("=" * 60)
        logger.info("파일럿 데이터 수집 시작")
        logger.info("=" * 60)

        # 1. 플랫폼 통계
        stats = self.collect_stats()
        save_json(stats, os.path.join(RAW_DATA_DIR, "pilot_stats.json"))
        logger.info(f"통계: 게시글 {stats.get('totalPosts', '?')}개, "
                     f"댓글 {stats.get('totalComments', '?')}개, "
                     f"에이전트 {stats.get('totalAgents', '?')}개")

        # 2. 게시글 수집
        posts = self.collect_posts(limit=post_limit)
        save_json(posts, os.path.join(RAW_DATA_DIR, "pilot_posts.json"))
        logger.info(f"게시글 {len(posts)}개 수집 완료")

        # 3. 에이전트 요약 생성
        agent_summary = self._build_agent_summary(posts)
        save_json(agent_summary, os.path.join(PROCESSED_DATA_DIR, "agent_summary.json"))
        logger.info(f"에이전트 {len(agent_summary)}명 요약 생성")

        # 4. 마당별 요약 생성
        submadang_summary = self._build_submadang_summary(posts)
        save_json(submadang_summary, os.path.join(PROCESSED_DATA_DIR, "submadang_summary.json"))
        logger.info(f"마당 {len(submadang_summary)}개 요약 생성")

        # 5. 상위 에이전트 상세 수집
        top_agents = sorted(agent_summary, key=lambda a: a["post_count"], reverse=True)[:10]
        logger.info(f"\n상위 {len(top_agents)}개 에이전트 상세 수집:")
        for agent in top_agents:
            agent_id = agent["author_id"]
            agent_name = agent["author_name"]
            logger.info(f"  {agent_name} ({agent['post_count']}개 글)")

            # 에이전트별 댓글 수집
            comments = self.collect_agent_comments(agent_id, limit=50)
            if comments:
                save_json(
                    comments,
                    os.path.join(RAW_DATA_DIR, f"agent_{agent_name}_comments.json"),
                )
                agent["comments_collected"] = len(comments)

        # 최종 요약 저장
        save_json(agent_summary, os.path.join(PROCESSED_DATA_DIR, "agent_summary.json"))

        result = {
            "timestamp": datetime.now().astimezone().isoformat(),
            "stats": stats,
            "posts_collected": len(posts),
            "agents_found": len(agent_summary),
            "submadangs_found": len(submadang_summary),
            "top_agents": [a["author_name"] for a in top_agents],
            "request_count": self._request_count,
        }
        save_json(result, os.path.join(RAW_DATA_DIR, "pilot_summary.json"))

        logger.info("=" * 60)
        logger.info(f"파일럿 수집 완료: {len(posts)}개 글, {len(agent_summary)}명 에이전트")
        logger.info(f"총 API 요청: {self._request_count}회")
        logger.info("=" * 60)

        return result

    def _build_agent_summary(self, posts: list[dict]) -> list[dict]:
        """게시글에서 에이전트 활동 요약 생성"""
        agents = {}
        for post in posts:
            aid = post.get("author_id", "unknown")
            if aid not in agents:
                agents[aid] = {
                    "author_id": aid,
                    "author_name": post.get("author_name", "unknown"),
                    "post_count": 0,
                    "total_upvotes": 0,
                    "total_downvotes": 0,
                    "total_comments": 0,
                    "submadangs": set(),
                    "first_post": post.get("created_at"),
                    "last_post": post.get("created_at"),
                }
            a = agents[aid]
            a["post_count"] += 1
            a["total_upvotes"] += post.get("upvotes", 0)
            a["total_downvotes"] += post.get("downvotes", 0)
            a["total_comments"] += post.get("comment_count", 0)
            a["submadangs"].add(post.get("submadang", "unknown"))
            if post.get("created_at"):
                if post["created_at"] < a["first_post"]:
                    a["first_post"] = post["created_at"]
                if post["created_at"] > a["last_post"]:
                    a["last_post"] = post["created_at"]

        result = []
        for a in agents.values():
            a["submadangs"] = sorted(a["submadangs"])
            a["avg_upvotes"] = round(a["total_upvotes"] / a["post_count"], 2) if a["post_count"] > 0 else 0
            result.append(a)
        return sorted(result, key=lambda x: x["post_count"], reverse=True)

    def _build_submadang_summary(self, posts: list[dict]) -> list[dict]:
        """게시글에서 마당별 요약 생성"""
        madangs = {}
        for post in posts:
            m = post.get("submadang", "unknown")
            if m not in madangs:
                madangs[m] = {
                    "name": m,
                    "post_count": 0,
                    "total_upvotes": 0,
                    "total_comments": 0,
                    "unique_agents": set(),
                }
            md = madangs[m]
            md["post_count"] += 1
            md["total_upvotes"] += post.get("upvotes", 0)
            md["total_comments"] += post.get("comment_count", 0)
            md["unique_agents"].add(post.get("author_id", "unknown"))

        result = []
        for md in madangs.values():
            md["unique_agents"] = len(md["unique_agents"])
            result.append(md)
        return sorted(result, key=lambda x: x["post_count"], reverse=True)


def save_json(data, filepath: str):
    """JSON 파일 저장"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    logger.info(f"  저장: {os.path.relpath(filepath)}")


def main():
    parser = argparse.ArgumentParser(description="봇마당 API 데이터 수집기")
    parser.add_argument(
        "--api-key",
        help="봇마당 API 키 (댓글 수집 시 필요)",
        default=os.environ.get("BOTMADANG_API_KEY"),
    )

    subparsers = parser.add_subparsers(dest="command", help="수집 명령")

    # posts
    p_posts = subparsers.add_parser("posts", help="게시글 수집")
    p_posts.add_argument("--limit", type=int, default=500, help="수집할 게시글 수")
    p_posts.add_argument("--submadang", help="특정 마당만 수집")
    p_posts.add_argument("--sort", help="정렬 기준")
    p_posts.add_argument("--output", help="출력 파일 경로")

    # agent-posts
    p_agent = subparsers.add_parser("agent-posts", help="에이전트 게시글 수집")
    p_agent.add_argument("--agent-id", required=True, help="에이전트 ID")
    p_agent.add_argument("--limit", type=int, default=100, help="수집할 게시글 수")
    p_agent.add_argument("--output", help="출력 파일 경로")

    # stats
    subparsers.add_parser("stats", help="플랫폼 통계 조회")

    # pilot
    p_pilot = subparsers.add_parser("pilot", help="파일럿 데이터 수집")
    p_pilot.add_argument("--limit", type=int, default=500, help="수집할 게시글 수")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    collector = BotmadangCollector(api_key=args.api_key)

    if args.command == "posts":
        posts = collector.collect_posts(
            limit=args.limit,
            submadang=args.submadang,
            sort=args.sort,
        )
        output = args.output or os.path.join(RAW_DATA_DIR, "posts.json")
        save_json(posts, output)
        print(f"수집 완료: {len(posts)}개 게시글 → {output}")

    elif args.command == "agent-posts":
        posts = collector.collect_agent_posts(args.agent_id, limit=args.limit)
        output = args.output or os.path.join(RAW_DATA_DIR, f"agent_{args.agent_id}_posts.json")
        save_json(posts, output)
        print(f"수집 완료: {len(posts)}개 게시글 → {output}")

    elif args.command == "stats":
        stats = collector.collect_stats()
        print(json.dumps(stats, indent=2, ensure_ascii=False))

    elif args.command == "pilot":
        result = collector.collect_pilot(post_limit=args.limit)
        print(f"\n파일럿 수집 완료!")
        print(f"  게시글: {result['posts_collected']}개")
        print(f"  에이전트: {result['agents_found']}명")
        print(f"  마당: {result['submadangs_found']}개")


if __name__ == "__main__":
    main()
