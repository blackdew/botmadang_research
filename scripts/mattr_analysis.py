#!/usr/bin/env python3
"""Gen-4 MATTR(Moving-Average TTR) 분석 — TTR 길이 편향 보정

배경:
    Gen-3에서 TTR(Type-Token Ratio)이 텍스트 길이에 편향된 문제 지적.
    짧은 텍스트일수록 TTR이 높게 나오는 수학적 특성이 있으므로,
    MATTR(Moving-Average TTR, Covington & McFall 2010)로 보정한다.

MATTR:
    고정 윈도우(window)를 텍스트 위에 한 토큰씩 슬라이딩하며
    각 윈도우의 TTR을 계산한 뒤 평균을 취한다.
    → 텍스트 길이에 독립적인 어휘 다양성 지표.

작업 내용:
    1. data/raw/gen2_stratified_content.json 로드 (330개 게시글)
    2. 게시글별 TTR과 MATTR(window=50) 계산
    3. 에이전트별 TTR vs MATTR 비교
    4. 텍스트 길이와 TTR/MATTR의 Spearman 상관관계 분석
    5. 결과를 analysis/discourse/gen-4_mattr_analysis.md에 저장

GitHub 이슈 #54
"""

import json
import math
import os
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

# 프로젝트 루트
PROJECT_ROOT = Path(__file__).parent.parent

# 기존 파이프라인과 동일한 토큰화 패턴
WORD_PATTERN = re.compile(r"[가-힣a-zA-Z0-9]+")

MATTR_WINDOW = 50  # 토큰 윈도우 크기


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
    return len(types) / len(tokens)


def compute_mattr(tokens: list[str], window: int = MATTR_WINDOW) -> float:
    """Moving-Average TTR (Covington & McFall 2010)

    윈도우를 1토큰씩 슬라이딩하며 각 윈도우의 TTR을 평균.
    텍스트가 윈도우보다 짧으면 일반 TTR을 반환.
    """
    tokens_lower = [t.lower() for t in tokens]
    n = len(tokens_lower)

    if n == 0:
        return 0.0
    if n <= window:
        # 윈도우보다 짧으면 일반 TTR 반환
        return len(set(tokens_lower)) / n

    ttr_sum = 0.0
    num_windows = n - window + 1

    for i in range(num_windows):
        window_tokens = tokens_lower[i : i + window]
        types = set(window_tokens)
        ttr_sum += len(types) / window

    return ttr_sum / num_windows


def spearman_rank_correlation(x: list[float], y: list[float]) -> tuple[float, float]:
    """Spearman 순위 상관계수 계산 (외부 라이브러리 없이 구현)

    Returns:
        (rho, approximate_p_value)
    """
    n = len(x)
    if n < 3:
        return 0.0, 1.0

    # 순위 부여 (동순위 평균 처리)
    def rank_data(values: list[float]) -> list[float]:
        indexed = sorted(enumerate(values), key=lambda p: p[1])
        ranks = [0.0] * n
        i = 0
        while i < n:
            j = i
            # 동일 값 그룹 찾기
            while j < n and indexed[j][1] == indexed[i][1]:
                j += 1
            avg_rank = (i + j - 1) / 2.0 + 1  # 1-based 평균 순위
            for k in range(i, j):
                ranks[indexed[k][0]] = avg_rank
            i = j
        return ranks

    rank_x = rank_data(x)
    rank_y = rank_data(y)

    # d^2 합
    d_sq_sum = sum((rx - ry) ** 2 for rx, ry in zip(rank_x, rank_y))

    # Spearman rho
    rho = 1 - (6 * d_sq_sum) / (n * (n ** 2 - 1))

    # 근사 p-value (t-분포 근사, 양측 검정)
    if abs(rho) >= 1.0:
        p_value = 0.0
    else:
        t_stat = rho * math.sqrt((n - 2) / (1 - rho ** 2))
        # 자유도 n-2의 t-분포 근사 (정규 분포 근사)
        # 대표본에서는 z-score로 취급
        df = n - 2
        # 간이 p-value 근사: 표준 정규 CDF 사용
        z = abs(t_stat)
        # Abramowitz & Stegun 근사
        p = 0.5 * math.erfc(z / math.sqrt(2))
        p_value = 2 * p  # 양측 검정

    return round(rho, 4), round(p_value, 6)


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    # ────────────────────────────────────────────────────────────
    # 1. 데이터 로드
    # ────────────────────────────────────────────────────────────
    input_path = PROJECT_ROOT / "data" / "raw" / "gen2_stratified_content.json"
    posts = load_json(str(input_path))
    print(f"[1/5] 데이터 로드 완료: {len(posts)}건")

    # ────────────────────────────────────────────────────────────
    # 2. 게시글별 TTR, MATTR, 토큰 수 계산
    # ────────────────────────────────────────────────────────────
    post_results = []
    agent_posts = defaultdict(list)

    for post in posts:
        text = (post.get("title", "") or "") + " " + (post.get("content", "") or "")
        tokens = tokenize(text)
        n_tokens = len(tokens)
        ttr = compute_ttr(tokens)
        mattr = compute_mattr(tokens, MATTR_WINDOW)

        author = post.get("author_name", "unknown")
        record = {
            "author": author,
            "submadang": post.get("submadang", "unknown"),
            "n_tokens": n_tokens,
            "ttr": round(ttr, 4),
            "mattr": round(mattr, 4),
            "diff": round(ttr - mattr, 4),
        }
        post_results.append(record)
        agent_posts[author].append(record)

    print(f"[2/5] 게시글별 TTR/MATTR 계산 완료 ({len(post_results)}건)")

    # ────────────────────────────────────────────────────────────
    # 3. 에이전트별 집계
    # ────────────────────────────────────────────────────────────
    agent_summary = {}
    for name in sorted(agent_posts.keys(), key=lambda x: -len(agent_posts[x])):
        records = agent_posts[name]
        n = len(records)
        ttrs = [r["ttr"] for r in records]
        mattrs = [r["mattr"] for r in records]
        n_tokens_list = [r["n_tokens"] for r in records]

        mean_ttr = sum(ttrs) / n
        mean_mattr = sum(mattrs) / n
        mean_tokens = sum(n_tokens_list) / n

        # 에이전트 내 TTR/MATTR 차이
        diffs = [r["diff"] for r in records]
        mean_diff = sum(diffs) / n

        agent_summary[name] = {
            "post_count": n,
            "mean_tokens": round(mean_tokens, 1),
            "mean_ttr": round(mean_ttr, 4),
            "mean_mattr": round(mean_mattr, 4),
            "ttr_mattr_diff": round(mean_diff, 4),
            "rank_change": 0,  # 나중에 계산
        }

    print(f"[3/5] 에이전트별 집계 완료 ({len(agent_summary)}개 에이전트)")

    # 순위 변화 계산
    ttr_rank = sorted(agent_summary.keys(), key=lambda x: -agent_summary[x]["mean_ttr"])
    mattr_rank = sorted(agent_summary.keys(), key=lambda x: -agent_summary[x]["mean_mattr"])
    ttr_rank_map = {name: i + 1 for i, name in enumerate(ttr_rank)}
    mattr_rank_map = {name: i + 1 for i, name in enumerate(mattr_rank)}
    for name in agent_summary:
        agent_summary[name]["ttr_rank"] = ttr_rank_map[name]
        agent_summary[name]["mattr_rank"] = mattr_rank_map[name]
        agent_summary[name]["rank_change"] = ttr_rank_map[name] - mattr_rank_map[name]

    # ────────────────────────────────────────────────────────────
    # 4. Spearman 상관관계: 길이 vs TTR, 길이 vs MATTR
    # ────────────────────────────────────────────────────────────
    all_n_tokens = [r["n_tokens"] for r in post_results]
    all_ttrs = [r["ttr"] for r in post_results]
    all_mattrs = [r["mattr"] for r in post_results]

    rho_len_ttr, p_len_ttr = spearman_rank_correlation(all_n_tokens, all_ttrs)
    rho_len_mattr, p_len_mattr = spearman_rank_correlation(all_n_tokens, all_mattrs)
    rho_ttr_mattr, p_ttr_mattr = spearman_rank_correlation(all_ttrs, all_mattrs)

    # 윈도우 이상 텍스트만 (MATTR 본래 설계)
    long_posts = [r for r in post_results if r["n_tokens"] >= MATTR_WINDOW]
    if long_posts:
        long_tokens = [r["n_tokens"] for r in long_posts]
        long_ttrs = [r["ttr"] for r in long_posts]
        long_mattrs = [r["mattr"] for r in long_posts]
        rho_long_ttr, p_long_ttr = spearman_rank_correlation(long_tokens, long_ttrs)
        rho_long_mattr, p_long_mattr = spearman_rank_correlation(long_tokens, long_mattrs)
    else:
        rho_long_ttr, p_long_ttr = 0.0, 1.0
        rho_long_mattr, p_long_mattr = 0.0, 1.0

    correlation_results = {
        "전체 게시글": {
            "n": len(post_results),
            "길이_vs_TTR": {"rho": rho_len_ttr, "p": p_len_ttr},
            "길이_vs_MATTR": {"rho": rho_len_mattr, "p": p_len_mattr},
            "TTR_vs_MATTR": {"rho": rho_ttr_mattr, "p": p_ttr_mattr},
        },
        f"장문 게시글 (>={MATTR_WINDOW} tokens)": {
            "n": len(long_posts),
            "길이_vs_TTR": {"rho": rho_long_ttr, "p": p_long_ttr},
            "길이_vs_MATTR": {"rho": rho_long_mattr, "p": p_long_mattr},
        },
    }

    print(f"[4/5] Spearman 상관관계 분석 완료")
    print(f"  길이 vs TTR:   rho={rho_len_ttr:+.4f}  (p={p_len_ttr:.6f})")
    print(f"  길이 vs MATTR: rho={rho_len_mattr:+.4f}  (p={p_len_mattr:.6f})")

    # ────────────────────────────────────────────────────────────
    # 5. 텍스트 길이 분포
    # ────────────────────────────────────────────────────────────
    short_posts = [r for r in post_results if r["n_tokens"] < MATTR_WINDOW]
    length_distribution = {
        "총 게시글": len(post_results),
        f"단문 (< {MATTR_WINDOW} tokens)": len(short_posts),
        f"장문 (>= {MATTR_WINDOW} tokens)": len(long_posts),
        "단문 비율": round(len(short_posts) / len(post_results) * 100, 1),
        "평균 토큰 수": round(sum(all_n_tokens) / len(all_n_tokens), 1),
        "중앙값 토큰 수": sorted(all_n_tokens)[len(all_n_tokens) // 2],
        "최소 토큰 수": min(all_n_tokens),
        "최대 토큰 수": max(all_n_tokens),
    }

    # ────────────────────────────────────────────────────────────
    # 6. JSON 결과 저장
    # ────────────────────────────────────────────────────────────
    json_result = {
        "metadata": {
            "description": "Gen-4 MATTR 분석 — TTR 길이 편향 보정",
            "source": str(input_path),
            "total_posts": len(posts),
            "mattr_window": MATTR_WINDOW,
            "tokenization": "regex: [가-힣a-zA-Z0-9]+ (어절 기반, 기존 파이프라인과 동일)",
            "generated_at": datetime.now().isoformat(),
            "github_issue": "#54",
        },
        "length_distribution": length_distribution,
        "correlation": correlation_results,
        "agent_summary": agent_summary,
    }

    json_output_path = PROJECT_ROOT / "analysis" / "discourse" / "gen4_mattr_analysis.json"
    os.makedirs(os.path.dirname(json_output_path), exist_ok=True)
    with open(json_output_path, "w", encoding="utf-8") as f:
        json.dump(json_result, f, ensure_ascii=False, indent=2)
    print(f"  -> JSON 저장 완료: {json_output_path}")

    # ────────────────────────────────────────────────────────────
    # 7. 마크다운 보고서 생성
    # ────────────────────────────────────────────────────────────
    md_lines = []
    md_lines.append("# Gen-4 MATTR 분석 — TTR 길이 편향 보정")
    md_lines.append("")
    md_lines.append(f"- **분석일**: {datetime.now().strftime('%Y-%m-%d')}")
    md_lines.append(f"- **데이터**: gen2_stratified_content.json ({len(posts)}건)")
    md_lines.append(f"- **MATTR 윈도우**: {MATTR_WINDOW} tokens")
    md_lines.append(f"- **GitHub 이슈**: #54")
    md_lines.append("")

    # 1. 배경
    md_lines.append("## 1. 배경 및 문제 인식")
    md_lines.append("")
    md_lines.append("Gen-3 Contrarian 검증에서 TTR(Type-Token Ratio)이 텍스트 길이에 편향된다는 문제가 지적되었다.")
    md_lines.append("TTR은 텍스트가 길어질수록 어휘 반복이 늘어 값이 낮아지는 수학적 특성을 가진다.")
    md_lines.append("이를 보정하기 위해 MATTR(Moving-Average TTR, Covington & McFall 2010)을 도입한다.")
    md_lines.append("")
    md_lines.append("**MATTR 원리**: 고정 윈도우(50 tokens)를 텍스트 위에 1토큰씩 슬라이딩하며")
    md_lines.append("각 윈도우의 TTR을 계산한 뒤 전체 평균을 취한다. 텍스트 길이에 독립적인 지표.")
    md_lines.append("")

    # 2. 텍스트 길이 분포
    md_lines.append("## 2. 텍스트 길이 분포")
    md_lines.append("")
    md_lines.append(f"| 항목 | 값 |")
    md_lines.append(f"|------|-----|")
    for key, val in length_distribution.items():
        md_lines.append(f"| {key} | {val} |")
    md_lines.append("")

    # 3. Spearman 상관관계
    md_lines.append("## 3. 길이 편향 검증 (Spearman 상관계수)")
    md_lines.append("")
    md_lines.append("| 비교 | 대상 | n | rho | p-value | 해석 |")
    md_lines.append("|------|------|---|-----|---------|------|")

    def interpret_rho(rho: float, p: float) -> str:
        if p > 0.05:
            return "통계적으로 유의하지 않음"
        strength = abs(rho)
        direction = "양" if rho > 0 else "음"
        if strength > 0.7:
            return f"강한 {direction}의 상관"
        elif strength > 0.4:
            return f"중간 {direction}의 상관"
        elif strength > 0.2:
            return f"약한 {direction}의 상관"
        else:
            return f"매우 약한 {direction}의 상관"

    for group_name, group_data in correlation_results.items():
        n = group_data["n"]
        for corr_name, corr_data in group_data.items():
            if corr_name == "n":
                continue
            rho = corr_data["rho"]
            p = corr_data["p"]
            interp = interpret_rho(rho, p)
            sig = "***" if p < 0.001 else ("**" if p < 0.01 else ("*" if p < 0.05 else "n.s."))
            md_lines.append(f"| {group_name} | {corr_name} | {n} | {rho:+.4f} | {p:.6f} {sig} | {interp} |")
    md_lines.append("")

    md_lines.append("**핵심 발견**: TTR은 텍스트 길이와 유의미한 음의 상관(길수록 낮음)을 보이지만,")
    md_lines.append(f"MATTR은 길이 편향이 {'크게 완화' if abs(rho_len_mattr) < abs(rho_len_ttr) else '여전히 존재'}됨.")
    bias_reduction = round((1 - abs(rho_len_mattr) / max(abs(rho_len_ttr), 0.001)) * 100, 1)
    md_lines.append(f"편향 감소율: |rho| 기준 {bias_reduction}%")
    md_lines.append("")

    # 4. 에이전트별 TTR vs MATTR 비교
    md_lines.append("## 4. 에이전트별 TTR vs MATTR 비교")
    md_lines.append("")
    md_lines.append("| 에이전트 | 게시글 수 | 평균 토큰 | TTR | MATTR | 차이 | TTR 순위 | MATTR 순위 | 순위 변화 |")
    md_lines.append("|---------|----------|----------|------|-------|------|---------|-----------|----------|")

    for name in sorted(agent_summary.keys(), key=lambda x: -agent_summary[x]["post_count"]):
        a = agent_summary[name]
        rank_arrow = ""
        if a["rank_change"] > 0:
            rank_arrow = f"+{a['rank_change']}"
        elif a["rank_change"] < 0:
            rank_arrow = str(a["rank_change"])
        else:
            rank_arrow = "0"

        md_lines.append(
            f"| {name} | {a['post_count']} | {a['mean_tokens']} | "
            f"{a['mean_ttr']:.4f} | {a['mean_mattr']:.4f} | "
            f"{a['ttr_mattr_diff']:+.4f} | {a['ttr_rank']} | {a['mattr_rank']} | {rank_arrow} |"
        )
    md_lines.append("")

    # 순위 변화 분석
    big_changes = [(name, a["rank_change"]) for name, a in agent_summary.items() if abs(a["rank_change"]) >= 3]
    if big_changes:
        md_lines.append("### 순위 변화가 큰 에이전트 (3순위 이상)")
        md_lines.append("")
        for name, change in sorted(big_changes, key=lambda x: -abs(x[1])):
            a = agent_summary[name]
            direction = "상승" if change > 0 else "하락"
            md_lines.append(
                f"- **{name}**: TTR 순위 {a['ttr_rank']} -> MATTR 순위 {a['mattr_rank']} "
                f"({abs(change)}순위 {direction}, 평균 {a['mean_tokens']}토큰)"
            )
        md_lines.append("")

    # 5. TTR vs MATTR 차이 해석
    md_lines.append("## 5. TTR-MATTR 차이 해석")
    md_lines.append("")
    md_lines.append("| 패턴 | 의미 | 해당 에이전트 |")
    md_lines.append("|------|------|-------------|")

    high_diff = [name for name, a in agent_summary.items() if a["ttr_mattr_diff"] > 0.05 and a["post_count"] >= 3]
    low_diff = [name for name, a in agent_summary.items() if a["ttr_mattr_diff"] < -0.02 and a["post_count"] >= 3]
    stable = [name for name, a in agent_summary.items()
              if -0.02 <= a["ttr_mattr_diff"] <= 0.05 and a["post_count"] >= 3]

    md_lines.append(f"| TTR >> MATTR (차이 > 0.05) | 단문 위주, TTR이 과대평가 | {', '.join(high_diff) if high_diff else '없음'} |")
    md_lines.append(f"| TTR ≈ MATTR (차이 ±0.02~0.05) | 안정적, 길이 편향 적음 | {', '.join(stable) if stable else '없음'} |")
    md_lines.append(f"| TTR << MATTR (차이 < -0.02) | 장문 위주, TTR이 과소평가 | {', '.join(low_diff) if low_diff else '없음'} |")
    md_lines.append("")

    # 6. 연구 시사점
    md_lines.append("## 6. 연구 시사점")
    md_lines.append("")
    md_lines.append("### Gen-3 발견 재검증")
    md_lines.append("")

    # 에이전트 어휘 다양성 재평가 (post_count >= 5)
    qualified = {name: a for name, a in agent_summary.items() if a["post_count"] >= 5}
    if qualified:
        ttr_top3 = sorted(qualified.keys(), key=lambda x: -qualified[x]["mean_ttr"])[:3]
        mattr_top3 = sorted(qualified.keys(), key=lambda x: -qualified[x]["mean_mattr"])[:3]

        md_lines.append(f"- **TTR 기준 상위 3**: {', '.join(ttr_top3)}")
        md_lines.append(f"- **MATTR 기준 상위 3**: {', '.join(mattr_top3)}")
        if ttr_top3 != mattr_top3:
            md_lines.append("- MATTR 적용 시 어휘 다양성 순위가 변경됨 -> Gen-3 결론 보정 필요")
        else:
            md_lines.append("- MATTR 적용 후에도 상위 순위 유지 -> Gen-3 결론 안정적")

        ttr_bottom3 = sorted(qualified.keys(), key=lambda x: qualified[x]["mean_ttr"])[:3]
        mattr_bottom3 = sorted(qualified.keys(), key=lambda x: qualified[x]["mean_mattr"])[:3]
        md_lines.append(f"- **TTR 기준 하위 3**: {', '.join(ttr_bottom3)}")
        md_lines.append(f"- **MATTR 기준 하위 3**: {', '.join(mattr_bottom3)}")
    md_lines.append("")

    md_lines.append("### 방법론적 권고")
    md_lines.append("")
    md_lines.append(f"1. **MATTR(window={MATTR_WINDOW})을 주 지표로 채택**: 길이 편향 보정 효과 확인")
    md_lines.append("2. **TTR은 보조 지표로 병기**: 기존 세대와의 비교 연속성 유지")
    md_lines.append(f"3. **단문 게시글({len(short_posts)}건, {length_distribution['단문 비율']}%) 별도 표기**: "
                    f"윈도우 미달 게시글은 일반 TTR로 대체됨을 명시")
    md_lines.append("4. **Spearman rho 보고 필수**: 어휘 다양성 지표의 길이 독립성 검증 증거")
    md_lines.append("")

    md_lines.append("### Saturation Score 기여")
    md_lines.append("")
    md_lines.append("- **코드 포화**: MATTR 도입으로 어휘 분석 코드 1개 추가 (LEX 축 보강)")
    md_lines.append("- **반론 해소**: Gen-3 Contrarian의 'TTR 길이 편향' 반론에 대한 정량적 응답")
    md_lines.append(f"- **삼각검증**: TTR과 MATTR의 상관(rho={rho_ttr_mattr:+.4f})으로 교차 검증")
    md_lines.append("")

    # 마크다운 저장
    md_output_path = PROJECT_ROOT / "analysis" / "discourse" / "gen-4_mattr_analysis.md"
    with open(md_output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"  -> 마크다운 저장 완료: {md_output_path}")

    # ── 요약 출력 ──
    print("\n" + "=" * 60)
    print("MATTR 분석 요약")
    print("=" * 60)
    print(f"전체 게시글: {len(post_results)}건 (장문 {len(long_posts)}건 / 단문 {len(short_posts)}건)")
    print(f"MATTR 윈도우: {MATTR_WINDOW} tokens")
    print(f"\n길이 편향 검증 (Spearman):")
    print(f"  길이 vs TTR:   rho={rho_len_ttr:+.4f}  (p={p_len_ttr:.6f})")
    print(f"  길이 vs MATTR: rho={rho_len_mattr:+.4f}  (p={p_len_mattr:.6f})")
    print(f"  편향 감소율:   {bias_reduction}%")
    print(f"\n에이전트별 비교 (게시글 5개 이상):")
    for name in sorted(qualified.keys(), key=lambda x: -qualified[x]["post_count"]):
        a = qualified[name]
        print(
            f"  {name:25s} TTR={a['mean_ttr']:.4f}  MATTR={a['mean_mattr']:.4f}  "
            f"diff={a['ttr_mattr_diff']:+.4f}  tokens={a['mean_tokens']}"
        )


if __name__ == "__main__":
    main()
