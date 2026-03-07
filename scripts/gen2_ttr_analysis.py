#!/usr/bin/env python3
"""Gen-2 균등 샘플(330건)에 대한 어휘 다양성(TTR) 분석

작업 내용:
    1. data/raw/gen2_stratified_content.json 로드 (330개 게시글)
    2. 에이전트별 TTR(Type-Token Ratio) 계산 (어절 기반)
    3. 마당별 TTR 비교
    4. 고빈도 어휘 TOP 30 추출 (전체 + 에이전트별 TOP 10)
    5. Gen-1 vs Gen-2 TTR 비교

결과: analysis/discourse/gen2/ttr_analysis.json

GitHub 이슈 #30
"""

import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

# 프로젝트 루트
PROJECT_ROOT = Path(__file__).parent.parent

# 기존 파이프라인과 동일한 토큰화 패턴
WORD_PATTERN = re.compile(r"[가-힣a-zA-Z0-9]+")


def tokenize(text: str) -> list[str]:
    """텍스트를 어절(토큰) 목록으로 분리. 기존 파이프라인과 동일."""
    if not text:
        return []
    return WORD_PATTERN.findall(text)


def compute_ttr(tokens: list[str]) -> float:
    """Type-Token Ratio: 고유 어절 수 / 전체 어절 수"""
    if not tokens:
        return 0.0
    types = set(t.lower() for t in tokens)
    return round(len(types) / len(tokens), 4)


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: Any, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  -> 저장 완료: {path}")


def main():
    # ────────────────────────────────────────────────────────────
    # 1. 데이터 로드
    # ────────────────────────────────────────────────────────────
    input_path = PROJECT_ROOT / "data" / "raw" / "gen2_stratified_content.json"
    posts = load_json(str(input_path))
    print(f"[1/5] 데이터 로드 완료: {len(posts)}건")

    # ────────────────────────────────────────────────────────────
    # 2. 게시글별 토큰화 + TTR 계산
    # ────────────────────────────────────────────────────────────
    all_tokens: list[str] = []
    agent_tokens: dict[str, list[str]] = defaultdict(list)
    agent_post_ttrs: dict[str, list[float]] = defaultdict(list)
    madang_tokens: dict[str, list[str]] = defaultdict(list)
    madang_post_ttrs: dict[str, list[float]] = defaultdict(list)

    for post in posts:
        # 제목 + 본문 합산 토큰화
        text = (post.get("title", "") or "") + " " + (post.get("content", "") or "")
        tokens = tokenize(text)
        tokens_lower = [t.lower() for t in tokens]
        ttr = compute_ttr(tokens)

        author = post.get("author_name", "unknown")
        madang = post.get("submadang", "unknown")

        all_tokens.extend(tokens_lower)
        agent_tokens[author].extend(tokens_lower)
        agent_post_ttrs[author].append(ttr)
        madang_tokens[madang].extend(tokens_lower)
        madang_post_ttrs[madang].append(ttr)

    # 전체 TTR
    overall_unique = len(set(all_tokens))
    overall_total = len(all_tokens)
    overall_ttr = round(overall_unique / overall_total, 4) if overall_total > 0 else 0.0
    print(f"[2/5] TTR 계산 완료 — 전체 TTR: {overall_ttr} (고유 {overall_unique} / 전체 {overall_total})")

    # ────────────────────────────────────────────────────────────
    # 2-1. 에이전트별 TTR
    # ────────────────────────────────────────────────────────────
    by_agent = {}
    for name in sorted(agent_post_ttrs.keys(), key=lambda x: -len(agent_post_ttrs[x])):
        ttrs = agent_post_ttrs[name]
        n = len(ttrs)
        sorted_ttrs = sorted(ttrs)
        tokens_all = agent_tokens[name]
        unique_count = len(set(tokens_all))
        total_count = len(tokens_all)
        corpus_ttr = round(unique_count / total_count, 4) if total_count > 0 else 0.0

        mean_ttr = round(sum(ttrs) / n, 4) if n > 0 else 0.0
        median_idx = n // 2
        median_ttr = round(
            (sorted_ttrs[median_idx] + sorted_ttrs[median_idx - 1]) / 2, 4
        ) if n > 1 and n % 2 == 0 else (sorted_ttrs[median_idx] if n > 0 else 0.0)

        by_agent[name] = {
            "post_count": n,
            "mean_ttr": mean_ttr,
            "median_ttr": median_ttr,
            "min_ttr": sorted_ttrs[0] if sorted_ttrs else 0.0,
            "max_ttr": sorted_ttrs[-1] if sorted_ttrs else 0.0,
            "corpus_ttr": corpus_ttr,
            "unique_tokens": unique_count,
            "total_tokens": total_count,
        }

    # ────────────────────────────────────────────────────────────
    # 3. 마당별 TTR
    # ────────────────────────────────────────────────────────────
    by_madang = {}
    for madang in sorted(madang_post_ttrs.keys(), key=lambda x: -len(madang_post_ttrs[x])):
        ttrs = madang_post_ttrs[madang]
        n = len(ttrs)
        sorted_ttrs = sorted(ttrs)
        tokens_all = madang_tokens[madang]
        unique_count = len(set(tokens_all))
        total_count = len(tokens_all)
        corpus_ttr = round(unique_count / total_count, 4) if total_count > 0 else 0.0

        mean_ttr = round(sum(ttrs) / n, 4) if n > 0 else 0.0
        median_idx = n // 2
        median_ttr = round(
            (sorted_ttrs[median_idx] + sorted_ttrs[median_idx - 1]) / 2, 4
        ) if n > 1 and n % 2 == 0 else (sorted_ttrs[median_idx] if n > 0 else 0.0)

        by_madang[madang] = {
            "post_count": n,
            "mean_ttr": mean_ttr,
            "median_ttr": median_ttr,
            "min_ttr": sorted_ttrs[0] if sorted_ttrs else 0.0,
            "max_ttr": sorted_ttrs[-1] if sorted_ttrs else 0.0,
            "corpus_ttr": corpus_ttr,
            "unique_tokens": unique_count,
            "total_tokens": total_count,
        }
    print(f"[3/5] 마당별 TTR 비교 완료 — {len(by_madang)}개 마당")

    # ────────────────────────────────────────────────────────────
    # 4. 고빈도 어휘 TOP 30 (전체) + 에이전트별 TOP 10
    # ────────────────────────────────────────────────────────────
    # 불용어 (한국어 조사, 접속사, 기본 어휘)
    stopwords = {
        "이", "그", "저", "것", "수", "등", "및", "또", "더", "를",
        "을", "에", "의", "가", "는", "은", "로", "으로", "에서", "와",
        "과", "도", "만", "까지", "부터", "보다", "같은", "이런", "그런",
        "위해", "통해", "대한", "있는", "없는", "하는", "되는", "했다",
        "한다", "된다", "하고", "있다", "없다", "하다", "되다", "아닌",
        "합니다", "있습니다", "없습니다", "입니다", "됩니다", "하지",
        "있어요", "없어요", "이에요", "거예요", "인데요", "해요",
        "a", "the", "is", "are", "of", "to", "in", "and", "for", "it",
        "that", "this", "with", "on", "at", "by", "an", "be", "or", "as",
    }

    # 1글자 토큰 제거 + 불용어 제거 후 빈도 계산
    def filtered_counter(tokens_list: list[str]) -> Counter:
        return Counter(
            t for t in tokens_list
            if len(t) > 1 and t not in stopwords
        )

    overall_counter = filtered_counter(all_tokens)
    top_30_vocab = [
        {"rank": i + 1, "word": word, "count": count}
        for i, (word, count) in enumerate(overall_counter.most_common(30))
    ]

    agent_top10 = {}
    for name, tokens_list in agent_tokens.items():
        counter = filtered_counter(tokens_list)
        agent_top10[name] = [
            {"rank": i + 1, "word": word, "count": count}
            for i, (word, count) in enumerate(counter.most_common(10))
        ]
    print(f"[4/5] 고빈도 어휘 추출 완료 — 전체 TOP 30 + {len(agent_top10)}개 에이전트 TOP 10")

    # ────────────────────────────────────────────────────────────
    # 5. Gen-1 vs Gen-2 비교
    # ────────────────────────────────────────────────────────────
    gen1_path = PROJECT_ROOT / "analysis" / "discourse" / "ttr_by_agent.json"
    gen1_comparison = {}

    if gen1_path.exists():
        gen1_data = load_json(str(gen1_path))
        gen1_agents = gen1_data.get("ttr_by_agent", {})

        # 공통 에이전트에 대해 비교
        common_agents = set(gen1_agents.keys()) & set(by_agent.keys())
        comparison_details = {}
        for name in sorted(common_agents, key=lambda x: -by_agent[x]["post_count"]):
            g1 = gen1_agents[name]
            g2 = by_agent[name]
            diff = round(g2["mean_ttr"] - g1["mean_ttr"], 4)
            comparison_details[name] = {
                "gen1_mean_ttr": g1["mean_ttr"],
                "gen1_post_count": g1["post_count"],
                "gen2_mean_ttr": g2["mean_ttr"],
                "gen2_post_count": g2["post_count"],
                "ttr_change": diff,
                "direction": "increase" if diff > 0 else ("decrease" if diff < 0 else "stable"),
            }

        # Gen-1 전체 평균 TTR (가중 평균)
        gen1_all_mean = [
            g1["mean_ttr"]
            for g1 in gen1_agents.values()
            if g1["post_count"] >= 3
        ]
        gen1_overall_mean = round(sum(gen1_all_mean) / len(gen1_all_mean), 4) if gen1_all_mean else 0.0

        gen2_all_mean = [
            g2["mean_ttr"]
            for g2 in by_agent.values()
            if g2["post_count"] >= 3
        ]
        gen2_overall_mean = round(sum(gen2_all_mean) / len(gen2_all_mean), 4) if gen2_all_mean else 0.0

        gen1_comparison = {
            "gen1_source": str(gen1_path),
            "gen1_agent_count": len(gen1_agents),
            "gen2_agent_count": len(by_agent),
            "common_agent_count": len(common_agents),
            "gen1_overall_mean_ttr": gen1_overall_mean,
            "gen2_overall_mean_ttr": gen2_overall_mean,
            "overall_ttr_change": round(gen2_overall_mean - gen1_overall_mean, 4),
            "by_agent": comparison_details,
            "only_in_gen1": sorted(set(gen1_agents.keys()) - set(by_agent.keys())),
            "only_in_gen2": sorted(set(by_agent.keys()) - set(gen1_agents.keys())),
        }
        print(f"[5/5] Gen-1 vs Gen-2 비교 완료 — 공통 에이전트 {len(common_agents)}개")
    else:
        gen1_comparison = {"error": f"Gen-1 TTR 파일 없음: {gen1_path}"}
        print(f"[5/5] Gen-1 TTR 파일 없음: {gen1_path}")

    # ────────────────────────────────────────────────────────────
    # 결과 저장
    # ────────────────────────────────────────────────────────────
    result = {
        "metadata": {
            "description": "Gen-2 균등 샘플(330건) 어휘 다양성(TTR) 분석",
            "source": str(input_path),
            "total_posts": len(posts),
            "tokenization": "regex: [가-힣a-zA-Z0-9]+ (어절 기반, 기존 파이프라인과 동일)",
            "generated_at": datetime.now().isoformat(),
            "github_issue": "#30",
        },
        "overall_ttr": {
            "ttr": overall_ttr,
            "unique_tokens": overall_unique,
            "total_tokens": overall_total,
        },
        "by_agent": by_agent,
        "by_madang": by_madang,
        "top_30_vocab": top_30_vocab,
        "agent_top10_vocab": agent_top10,
        "gen1_comparison": gen1_comparison,
    }

    output_path = PROJECT_ROOT / "analysis" / "discourse" / "gen2" / "ttr_analysis.json"
    save_json(result, str(output_path))

    # ── 요약 출력 ──
    print("\n" + "=" * 60)
    print("TTR 분석 요약")
    print("=" * 60)
    print(f"전체 TTR: {overall_ttr} (고유 {overall_unique} / 전체 {overall_total})")
    print(f"\n에이전트별 TTR (상위 10):")
    for i, (name, info) in enumerate(list(by_agent.items())[:10]):
        print(f"  {i+1:2d}. {name:25s} mean={info['mean_ttr']:.4f}  corpus={info['corpus_ttr']:.4f}  (n={info['post_count']})")
    print(f"\n마당별 TTR:")
    for madang, info in by_madang.items():
        print(f"  {madang:20s} mean={info['mean_ttr']:.4f}  corpus={info['corpus_ttr']:.4f}  (n={info['post_count']})")
    print(f"\n고빈도 어휘 TOP 10:")
    for item in top_30_vocab[:10]:
        print(f"  {item['rank']:2d}. {item['word']:15s} ({item['count']}회)")
    if gen1_comparison and "overall_ttr_change" in gen1_comparison:
        print(f"\nGen-1 vs Gen-2 전체 평균 TTR 변화: {gen1_comparison['overall_ttr_change']:+.4f}")
        print(f"  Gen-1: {gen1_comparison['gen1_overall_mean_ttr']:.4f}")
        print(f"  Gen-2: {gen1_comparison['gen2_overall_mean_ttr']:.4f}")


if __name__ == "__main__":
    main()
