"""
봇마당 에이전트 상호작용 네트워크 분석 스크립트

사용법: python scripts/network_analysis.py

출력:
  analysis/network/interaction_graph.json  — 방향성 가중치 그래프 (엣지 + 노드 속성)
  analysis/network/centrality.json         — 중심성 지표 (degree, in/out, pagerank, betweenness)
  analysis/network/community.json          — 커뮤니티/그룹 분석 (마당별 밀도, 클리크)
  analysis/network/summary.json            — 네트워크 요약 통계
"""

from __future__ import annotations

import glob
import json
import math
import os
import sys
from collections import defaultdict
from datetime import datetime
from typing import Any

# ─────────────────────────────────────────
# 경로 설정
# ─────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "analysis", "network")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────────
# 데이터 로딩
# ─────────────────────────────────────────

def load_posts() -> dict[str, dict]:
    """pilot_posts.json 로드 → {post_id: post} 매핑 반환"""
    path = os.path.join(RAW_DIR, "pilot_posts.json")
    with open(path, encoding="utf-8") as f:
        posts = json.load(f)
    return {p["id"]: p for p in posts}


def load_agent_comments() -> dict[str, list[dict]]:
    """agent_*_comments.json 전체 로드 → {agent_name: [comment, ...]} 반환"""
    pattern = os.path.join(RAW_DIR, "agent_*_comments.json")
    result: dict[str, list[dict]] = {}
    for path in sorted(glob.glob(pattern)):
        basename = os.path.basename(path)
        # agent_BENZIE_comments.json → BENZIE
        agent_name = basename[len("agent_"):-len("_comments.json")]
        with open(path, encoding="utf-8") as f:
            result[agent_name] = json.load(f)
    return result


def load_agent_summary() -> dict[str, dict]:
    """agent_summary.json 로드 → {author_name: agent_info} 반환"""
    path = os.path.join(PROCESSED_DIR, "agent_summary.json")
    with open(path, encoding="utf-8") as f:
        agents = json.load(f)
    return {a["author_name"]: a for a in agents}


# ─────────────────────────────────────────
# 그래프 구축
# ─────────────────────────────────────────

def build_interaction_graph(
    post_map: dict[str, dict],
    agent_comments: dict[str, list[dict]],
    agent_summary: dict[str, dict],
) -> tuple[dict, dict, dict]:
    """
    방향성 가중치 그래프 구축.

    상호작용 정의: A가 B의 게시글에 댓글을 달면 A→B 엣지 (가중치 +1).
    자기 자신의 게시글에 단 댓글(자기 루프)도 포함하여 자기 참조 패턴 포착.

    Returns:
        edges: {(src, dst): weight}
        nodes: {agent_name: {id, post_count, ...}}
        edge_meta: {(src, dst): [{comment_id, post_id, submadang, created_at}]}
    """
    # 에이전트 이름 집합 (댓글 파일 기준)
    commenter_names = set(agent_comments.keys())

    # 노드 속성 초기화
    nodes: dict[str, dict] = {}
    for name, info in agent_summary.items():
        nodes[name] = {
            "author_id": info.get("author_id", ""),
            "author_name": name,
            "post_count": info.get("post_count", 0),
            "total_upvotes": info.get("total_upvotes", 0),
            "total_comments": info.get("total_comments", 0),
            "submadangs": info.get("submadangs", []),
            "has_comment_data": name in commenter_names,
        }

    # 에이전트 author_id → author_name 역매핑 (게시글 author 식별용)
    id_to_name: dict[str, str] = {
        info.get("author_id", ""): name
        for name, info in agent_summary.items()
        if info.get("author_id")
    }

    edges: dict[tuple[str, str], int] = defaultdict(int)
    edge_meta: dict[tuple[str, str], list[dict]] = defaultdict(list)
    unmatched_count = 0

    for commenter, comments in agent_comments.items():
        for comment in comments:
            post_id = comment.get("post_id")
            if not post_id:
                continue

            post = post_map.get(post_id)
            if post is None:
                # pilot_posts에 없는 게시글 (다른 페이지) → 스킵
                unmatched_count += 1
                continue

            post_author_id = post.get("author_id", "")
            post_author_name = post.get("author_name", "")

            # post_author를 agent_summary 기준으로 정규화
            normalized_author = id_to_name.get(post_author_id, post_author_name)

            key = (commenter, normalized_author)
            edges[key] += 1
            edge_meta[key].append({
                "comment_id": comment.get("id", ""),
                "post_id": post_id,
                "submadang": post.get("submadang", ""),
                "created_at": comment.get("created_at", ""),
                "upvotes": comment.get("upvotes", 0),
            })

            # 노드에 아직 없으면 게시글에서 발견된 author 추가
            if normalized_author not in nodes:
                nodes[normalized_author] = {
                    "author_id": post_author_id,
                    "author_name": normalized_author,
                    "post_count": 0,
                    "total_upvotes": 0,
                    "total_comments": 0,
                    "submadangs": [],
                    "has_comment_data": False,
                }

    print(f"  매칭 실패 댓글 수: {unmatched_count}개 (pilot_posts 범위 밖)")
    return dict(edges), nodes, dict(edge_meta)


# ─────────────────────────────────────────
# 중심성 계산 (순수 Python)
# ─────────────────────────────────────────

def compute_degree_centrality(
    edges: dict[tuple[str, str], int],
    nodes: dict[str, dict],
) -> dict[str, dict]:
    """
    In-degree, Out-degree, Total degree 계산.
    가중치(상호작용 횟수) 기반과 비가중치(연결 수) 기반 모두 계산.
    """
    in_degree: dict[str, int] = defaultdict(int)
    out_degree: dict[str, int] = defaultdict(int)
    in_weighted: dict[str, float] = defaultdict(float)
    out_weighted: dict[str, float] = defaultdict(float)
    in_neighbors: dict[str, set] = defaultdict(set)
    out_neighbors: dict[str, set] = defaultdict(set)

    for (src, dst), weight in edges.items():
        out_degree[src] += 1
        in_degree[dst] += 1
        out_weighted[src] += weight
        in_weighted[dst] += weight
        out_neighbors[src].add(dst)
        in_neighbors[dst].add(src)

    n = max(len(nodes) - 1, 1)  # 정규화 분모

    centrality: dict[str, dict] = {}
    for name in nodes:
        ind = in_degree.get(name, 0)
        outd = out_degree.get(name, 0)
        in_w = in_weighted.get(name, 0.0)
        out_w = out_weighted.get(name, 0.0)
        centrality[name] = {
            "in_degree": ind,
            "out_degree": outd,
            "total_degree": ind + outd,
            "in_degree_centrality": round(ind / n, 4),
            "out_degree_centrality": round(outd / n, 4),
            "total_degree_centrality": round((ind + outd) / (2 * n), 4),
            "in_weighted": in_w,
            "out_weighted": out_w,
            "total_weighted": in_w + out_w,
            "in_neighbor_count": len(in_neighbors.get(name, set())),
            "out_neighbor_count": len(out_neighbors.get(name, set())),
        }
    return centrality


def compute_pagerank(
    edges: dict[tuple[str, str], int],
    nodes: dict[str, dict],
    damping: float = 0.85,
    max_iter: int = 100,
    tol: float = 1e-6,
) -> dict[str, float]:
    """
    가중치 기반 PageRank (Power Iteration).
    에이전트의 글을 많이 댓글 받을수록 높은 PageRank.
    """
    node_list = list(nodes.keys())
    n = len(node_list)
    if n == 0:
        return {}

    # 가중치 기반 전이 확률 행렬
    # out_weight[src] = src에서 나가는 총 가중치
    out_weight_total: dict[str, float] = defaultdict(float)
    for (src, _), w in edges.items():
        out_weight_total[src] += w

    rank = {name: 1.0 / n for name in node_list}

    for iteration in range(max_iter):
        new_rank: dict[str, float] = {}
        for node in node_list:
            # 이 노드를 가리키는 엣지들에서 PageRank 받기
            incoming_sum = 0.0
            for (src, dst), w in edges.items():
                if dst == node:
                    total_out = out_weight_total.get(src, 0.0)
                    if total_out > 0:
                        incoming_sum += rank[src] * (w / total_out)
            new_rank[node] = (1 - damping) / n + damping * incoming_sum

        # 수렴 확인
        diff = sum(abs(new_rank[node] - rank[node]) for node in node_list)
        rank = new_rank
        if diff < tol:
            print(f"  PageRank 수렴: {iteration + 1}회 반복")
            break

    return {name: round(v, 6) for name, v in rank.items()}


def compute_betweenness(
    edges: dict[tuple[str, str], int],
    nodes: dict[str, dict],
) -> dict[str, float]:
    """
    근사 Betweenness Centrality (BFS 기반).
    노드 수가 적을 때 정확한 계산, 많을 때 샘플링 적용.

    Brandes 알고리즘 (비가중치 방향 그래프 버전).
    """
    node_list = list(nodes.keys())
    n = len(node_list)
    if n <= 2:
        return {name: 0.0 for name in node_list}

    # 인접 리스트 구성 (방향 그래프)
    adj: dict[str, list[str]] = defaultdict(list)
    for (src, dst) in edges:
        adj[src].append(dst)

    betweenness: dict[str, float] = {name: 0.0 for name in node_list}

    for s in node_list:
        # BFS
        stack: list[str] = []
        pred: dict[str, list[str]] = {v: [] for v in node_list}
        sigma: dict[str, float] = {v: 0.0 for v in node_list}
        dist: dict[str, int] = {v: -1 for v in node_list}

        sigma[s] = 1.0
        dist[s] = 0
        queue: list[str] = [s]

        while queue:
            v = queue.pop(0)
            stack.append(v)
            for w in adj.get(v, []):
                if w not in node_list:
                    continue
                if dist[w] < 0:
                    queue.append(w)
                    dist[w] = dist[v] + 1
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]
                    pred[w].append(v)

        # 역방향 누적
        delta: dict[str, float] = {v: 0.0 for v in node_list}
        while stack:
            w = stack.pop()
            for v in pred[w]:
                if sigma[w] > 0:
                    delta[v] += (sigma[v] / sigma[w]) * (1.0 + delta[w])
            if w != s:
                betweenness[w] += delta[w]

    # 정규화 (방향 그래프: (n-1)(n-2))
    norm = (n - 1) * (n - 2)
    if norm > 0:
        betweenness = {name: round(v / norm, 6) for name, v in betweenness.items()}

    return betweenness


# ─────────────────────────────────────────
# 상호작용 패턴 분석
# ─────────────────────────────────────────

def analyze_reciprocity(
    edges: dict[tuple[str, str], int],
) -> dict[str, Any]:
    """
    호혜성 분석: A↔B 양방향 상호작용 쌍 탐지.
    """
    reciprocal_pairs: list[dict] = []
    seen: set[frozenset] = set()

    for (a, b), w_ab in edges.items():
        if a == b:
            continue
        pair_key = frozenset([a, b])
        if pair_key in seen:
            continue
        w_ba = edges.get((b, a), 0)
        if w_ba > 0:
            seen.add(pair_key)
            reciprocal_pairs.append({
                "agent_a": a,
                "agent_b": b,
                "a_to_b": w_ab,
                "b_to_a": w_ba,
                "total_interactions": w_ab + w_ba,
                "reciprocity_ratio": round(
                    min(w_ab, w_ba) / max(w_ab, w_ba), 3
                ),
            })

    # 전체 호혜성 지수
    total_edges = len([k for k in edges.keys() if k[0] != k[1]])
    reciprocal_edges = len(reciprocal_pairs) * 2
    global_reciprocity = round(
        reciprocal_edges / total_edges if total_edges > 0 else 0.0, 4
    )

    reciprocal_pairs.sort(key=lambda x: -x["total_interactions"])

    return {
        "global_reciprocity": global_reciprocity,
        "reciprocal_pair_count": len(reciprocal_pairs),
        "total_directed_edges": total_edges,
        "pairs": reciprocal_pairs,
    }


def find_hubs_and_isolates(
    centrality: dict[str, dict],
    nodes: dict[str, dict],
) -> dict[str, Any]:
    """허브(최다 연결)와 고립 에이전트(상호작용 없음) 분석."""
    # 허브: total_weighted 기준 상위 5
    sorted_by_total = sorted(
        centrality.items(),
        key=lambda x: -x[1]["total_weighted"],
    )
    hubs = [
        {
            "agent": name,
            "total_weighted": stats["total_weighted"],
            "in_weighted": stats["in_weighted"],
            "out_weighted": stats["out_weighted"],
            "total_degree": stats["total_degree"],
        }
        for name, stats in sorted_by_total[:5]
    ]

    # 고립: total_degree == 0
    isolates = [
        name
        for name, stats in centrality.items()
        if stats["total_degree"] == 0
    ]

    # 순수 수신자 (댓글 데이터 없어서 out=0이지만 in>0)
    pure_receivers = [
        name
        for name, stats in centrality.items()
        if stats["in_degree"] > 0 and stats["out_degree"] == 0
        and not nodes.get(name, {}).get("has_comment_data", False)
    ]

    return {
        "top_hubs": hubs,
        "isolates": isolates,
        "isolate_count": len(isolates),
        "pure_receivers": pure_receivers,
        "pure_receiver_count": len(pure_receivers),
    }


# ─────────────────────────────────────────
# 커뮤니티 분석
# ─────────────────────────────────────────

def analyze_submadang_density(
    edge_meta: dict[tuple[str, str], list[dict]],
    nodes: dict[str, dict],
) -> list[dict]:
    """
    마당(submadang)별 상호작용 밀도.
    밀도 = 실제 상호작용 쌍 수 / 가능한 최대 쌍 수
    """
    # 마당별 상호작용 집계
    madang_edges: dict[str, dict[tuple[str, str], int]] = defaultdict(
        lambda: defaultdict(int)
    )
    madang_agents: dict[str, set] = defaultdict(set)

    for (src, dst), meta_list in edge_meta.items():
        for m in meta_list:
            sm = m.get("submadang", "unknown")
            madang_edges[sm][(src, dst)] += 1
            madang_agents[sm].add(src)
            madang_agents[sm].add(dst)

    result: list[dict] = []
    for madang, agent_set in sorted(
        madang_agents.items(), key=lambda x: -len(x[1])
    ):
        n_agents = len(agent_set)
        n_edges = len(madang_edges.get(madang, {}))
        total_interactions = sum(madang_edges.get(madang, {}).values())

        # 방향 그래프 최대 엣지 수: n*(n-1)
        max_edges = n_agents * (n_agents - 1) if n_agents > 1 else 1
        density = round(n_edges / max_edges, 4)

        result.append({
            "submadang": madang,
            "agent_count": n_agents,
            "edge_count": n_edges,
            "total_interactions": total_interactions,
            "density": density,
            "agents": sorted(agent_set),
        })

    return result


def find_cliques(
    edges: dict[tuple[str, str], int],
    nodes: dict[str, dict],
    min_size: int = 3,
) -> list[list[str]]:
    """
    무방향 그래프로 변환 후 Bron-Kerbosch 알고리즘으로 최대 클리크 탐색.
    self-loop 제외.
    """
    # 무방향 인접 리스트
    undirected: dict[str, set] = defaultdict(set)
    for (src, dst) in edges:
        if src != dst:
            undirected[src].add(dst)
            undirected[dst].add(src)

    node_list = [n for n in nodes if n in undirected]
    cliques: list[list[str]] = []

    def bron_kerbosch(R: set, P: set, X: set):
        if not P and not X:
            if len(R) >= min_size:
                cliques.append(sorted(R))
            return
        # 피벗: P∪X에서 이웃이 가장 많은 노드
        pivot = max(P | X, key=lambda v: len(undirected.get(v, set()) & P))
        for v in list(P - undirected.get(pivot, set())):
            bron_kerbosch(
                R | {v},
                P & undirected.get(v, set()),
                X & undirected.get(v, set()),
            )
            P = P - {v}
            X = X | {v}

    bron_kerbosch(set(), set(node_list), set())
    # 최대 클리크만 (중복 제거 포함)
    cliques.sort(key=lambda c: -len(c))
    return cliques


def simple_community_detection(
    edges: dict[tuple[str, str], int],
    nodes: dict[str, dict],
) -> list[dict]:
    """
    연결 컴포넌트 기반 커뮤니티 탐지 (무방향 변환 후).
    NetworkX 없이 Union-Find로 구현.
    """
    parent: dict[str, str] = {name: name for name in nodes}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: str, y: str):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    for (src, dst) in edges:
        if src in parent and dst in parent and src != dst:
            union(src, dst)

    # 컴포넌트 수집
    components: dict[str, list[str]] = defaultdict(list)
    for name in nodes:
        root = find(name)
        components[root].append(name)

    result: list[dict] = []
    for root, members in sorted(
        components.items(), key=lambda x: -len(x[1])
    ):
        # 컴포넌트 내 엣지 수
        member_set = set(members)
        internal_edges = {
            (s, d): w
            for (s, d), w in edges.items()
            if s in member_set and d in member_set and s != d
        }
        result.append({
            "community_id": root,
            "member_count": len(members),
            "members": sorted(members),
            "internal_edge_count": len(internal_edges),
            "internal_interaction_count": sum(internal_edges.values()),
        })

    return result


# ─────────────────────────────────────────
# 요약 통계 계산
# ─────────────────────────────────────────

def compute_network_summary(
    edges: dict[tuple[str, str], int],
    nodes: dict[str, dict],
    centrality: dict[str, dict],
    pagerank: dict[str, float],
    betweenness: dict[str, float],
    reciprocity_stats: dict,
    communities: list[dict],
    submadang_density: list[dict],
) -> dict:
    """전체 네트워크 요약 통계."""
    n_nodes = len(nodes)
    # 자기 루프 제외한 엣지
    non_self_edges = {(s, d): w for (s, d), w in edges.items() if s != d}
    n_edges = len(non_self_edges)
    total_interactions = sum(non_self_edges.values())

    # 자기 루프 (자기 글에 댓글)
    self_loops = {(s, d): w for (s, d), w in edges.items() if s == d}

    # 평균 가중치
    avg_weight = round(total_interactions / n_edges if n_edges > 0 else 0.0, 3)

    # 그래프 밀도
    max_edges = n_nodes * (n_nodes - 1) if n_nodes > 1 else 1
    density = round(n_edges / max_edges, 4)

    # 최고 PageRank 에이전트
    top_pagerank = sorted(pagerank.items(), key=lambda x: -x[1])[:3]
    # 최고 Betweenness 에이전트
    top_betweenness = sorted(betweenness.items(), key=lambda x: -x[1])[:3]
    # 최다 상호작용 엣지
    top_edges = sorted(
        non_self_edges.items(), key=lambda x: -x[1]
    )[:5]

    # 에이전트별 활동 요약
    agent_activity = []
    for name in sorted(nodes.keys()):
        c = centrality.get(name, {})
        agent_activity.append({
            "agent": name,
            "in_degree": c.get("in_degree", 0),
            "out_degree": c.get("out_degree", 0),
            "in_weighted": c.get("in_weighted", 0),
            "out_weighted": c.get("out_weighted", 0),
            "pagerank": pagerank.get(name, 0.0),
            "betweenness": betweenness.get(name, 0.0),
        })
    agent_activity.sort(key=lambda x: -x["in_weighted"])

    return {
        "generated_at": datetime.now().isoformat(),
        "node_count": n_nodes,
        "edge_count": n_edges,
        "total_interactions": total_interactions,
        "self_loop_count": len(self_loops),
        "self_loop_interactions": sum(self_loops.values()),
        "average_edge_weight": avg_weight,
        "graph_density": density,
        "global_reciprocity": reciprocity_stats["global_reciprocity"],
        "reciprocal_pair_count": reciprocity_stats["reciprocal_pair_count"],
        "community_count": len(communities),
        "largest_community_size": communities[0]["member_count"] if communities else 0,
        "submadang_count": len(submadang_density),
        "top_pagerank_agents": [
            {"agent": a, "pagerank": round(v, 6)} for a, v in top_pagerank
        ],
        "top_betweenness_agents": [
            {"agent": a, "betweenness": round(v, 6)} for a, v in top_betweenness
        ],
        "top_interaction_edges": [
            {"from": s, "to": d, "weight": w} for (s, d), w in top_edges
        ],
        "agent_activity_table": agent_activity,
    }


# ─────────────────────────────────────────
# JSON 직렬화용 그래프 export
# ─────────────────────────────────────────

def build_graph_export(
    edges: dict[tuple[str, str], int],
    nodes: dict[str, dict],
    edge_meta: dict[tuple[str, str], list[dict]],
    centrality: dict[str, dict],
    pagerank: dict[str, float],
) -> dict:
    """
    시각화 도구(D3.js, Gephi, Cytoscape 등)에서 바로 사용 가능한
    nodes/links 형태로 export.
    """
    node_list = []
    for name, info in nodes.items():
        c = centrality.get(name, {})
        node_list.append({
            "id": name,
            "author_id": info.get("author_id", ""),
            "post_count": info.get("post_count", 0),
            "total_upvotes": info.get("total_upvotes", 0),
            "total_comments": info.get("total_comments", 0),
            "submadangs": info.get("submadangs", []),
            "has_comment_data": info.get("has_comment_data", False),
            "in_weighted": c.get("in_weighted", 0),
            "out_weighted": c.get("out_weighted", 0),
            "total_degree": c.get("total_degree", 0),
            "pagerank": pagerank.get(name, 0.0),
        })

    link_list = []
    for (src, dst), weight in edges.items():
        meta = edge_meta.get((src, dst), [])
        submadangs_used = list({m["submadang"] for m in meta if m.get("submadang")})
        link_list.append({
            "source": src,
            "target": dst,
            "weight": weight,
            "is_self_loop": src == dst,
            "submadangs": submadangs_used,
            "comment_ids": [m["comment_id"] for m in meta],
        })

    return {
        "graph_type": "directed_weighted",
        "description": "봇마당 에이전트 상호작용 네트워크 (A→B: A가 B의 게시글에 댓글을 단 횟수)",
        "generated_at": datetime.now().isoformat(),
        "nodes": sorted(node_list, key=lambda n: -n["total_degree"]),
        "links": sorted(link_list, key=lambda l: -l["weight"]),
        "stats": {
            "node_count": len(node_list),
            "link_count": len(link_list),
        },
    }


# ─────────────────────────────────────────
# NetworkX 선택적 활용
# ─────────────────────────────────────────

def try_networkx_analysis(
    edges: dict[tuple[str, str], int],
    nodes: dict[str, dict],
) -> dict | None:
    """
    NetworkX가 설치된 경우 추가 분석 수행.
    없으면 None 반환.
    """
    try:
        import networkx as nx  # type: ignore

        G = nx.DiGraph()
        G.add_nodes_from(nodes.keys())
        for (src, dst), weight in edges.items():
            G.add_edge(src, dst, weight=weight)

        result: dict = {"available": True, "version": nx.__version__}

        # NetworkX pagerank (검증용)
        try:
            pr = nx.pagerank(G, weight="weight")
            result["pagerank"] = {k: round(v, 6) for k, v in pr.items()}
        except Exception as e:
            result["pagerank_error"] = str(e)

        # HITS (Hubs & Authorities)
        try:
            h, a = nx.hits(G, max_iter=100)
            result["hits_hubs"] = {k: round(v, 6) for k, v in h.items()}
            result["hits_authorities"] = {k: round(v, 6) for k, v in a.items()}
        except Exception as e:
            result["hits_error"] = str(e)

        return result

    except ImportError:
        return None


# ─────────────────────────────────────────
# 메인 실행
# ─────────────────────────────────────────

def main():
    print("=" * 60)
    print("봇마당 에이전트 상호작용 네트워크 분석")
    print("=" * 60)

    # 1. 데이터 로딩
    print("\n[1/6] 데이터 로딩 중...")
    post_map = load_posts()
    agent_comments = load_agent_comments()
    agent_summary = load_agent_summary()
    print(f"  게시글: {len(post_map)}개")
    print(f"  댓글 파일: {len(agent_comments)}개 에이전트")
    print(f"  에이전트 요약: {len(agent_summary)}개")

    # 2. 상호작용 그래프 구축
    print("\n[2/6] 상호작용 그래프 구축 중...")
    edges, nodes, edge_meta = build_interaction_graph(
        post_map, agent_comments, agent_summary
    )
    non_self = {k: v for k, v in edges.items() if k[0] != k[1]}
    print(f"  노드 수: {len(nodes)}개")
    print(f"  엣지 수: {len(non_self)}개 (자기 루프 제외)")
    print(f"  총 상호작용: {sum(non_self.values())}회")

    # 3. 중심성 계산
    print("\n[3/6] 중심성 계산 중...")
    centrality = compute_degree_centrality(edges, nodes)
    pagerank = compute_pagerank(edges, nodes)
    betweenness = compute_betweenness(edges, nodes)
    print(f"  PageRank 상위 3: {sorted(pagerank.items(), key=lambda x: -x[1])[:3]}")

    # 4. 상호작용 패턴 분석
    print("\n[4/6] 상호작용 패턴 분석 중...")
    reciprocity_stats = analyze_reciprocity(edges)
    hubs_isolates = find_hubs_and_isolates(centrality, nodes)
    print(f"  호혜성 쌍: {reciprocity_stats['reciprocal_pair_count']}쌍")
    print(f"  전체 호혜성 지수: {reciprocity_stats['global_reciprocity']}")
    print(f"  고립 에이전트: {hubs_isolates['isolate_count']}개")

    # 5. 커뮤니티 분석
    print("\n[5/6] 커뮤니티 분석 중...")
    submadang_density = analyze_submadang_density(edge_meta, nodes)
    cliques = find_cliques(edges, nodes, min_size=3)
    communities = simple_community_detection(edges, nodes)
    print(f"  마당 수: {len(submadang_density)}개")
    print(f"  클리크(≥3): {len(cliques)}개")
    print(f"  연결 컴포넌트: {len(communities)}개")

    # NetworkX 선택적 활용
    nx_result = try_networkx_analysis(edges, nodes)
    if nx_result:
        print(f"  NetworkX {nx_result['version']} 추가 분석 완료")
    else:
        print("  NetworkX 미설치 — 순수 Python으로 계산 완료")

    # 6. 결과 저장
    print("\n[6/6] 결과 저장 중...")

    # interaction_graph.json
    graph_export = build_graph_export(edges, nodes, edge_meta, centrality, pagerank)
    graph_path = os.path.join(OUTPUT_DIR, "interaction_graph.json")
    with open(graph_path, "w", encoding="utf-8") as f:
        json.dump(graph_export, f, ensure_ascii=False, indent=2)
    print(f"  저장: {graph_path}")

    # centrality.json
    centrality_export = {
        "generated_at": datetime.now().isoformat(),
        "method": "pure_python_brandes_pagerank",
        "agents": {},
    }
    for name in sorted(nodes.keys()):
        centrality_export["agents"][name] = {
            **centrality.get(name, {}),
            "pagerank": pagerank.get(name, 0.0),
            "betweenness": betweenness.get(name, 0.0),
        }
    if nx_result and "pagerank" in nx_result:
        centrality_export["networkx_pagerank"] = nx_result["pagerank"]
    if nx_result and "hits_hubs" in nx_result:
        centrality_export["networkx_hits_hubs"] = nx_result["hits_hubs"]
        centrality_export["networkx_hits_authorities"] = nx_result["hits_authorities"]

    centrality_path = os.path.join(OUTPUT_DIR, "centrality.json")
    with open(centrality_path, "w", encoding="utf-8") as f:
        json.dump(centrality_export, f, ensure_ascii=False, indent=2)
    print(f"  저장: {centrality_path}")

    # community.json
    community_export = {
        "generated_at": datetime.now().isoformat(),
        "submadang_density": submadang_density,
        "cliques": {
            "method": "bron_kerbosch_undirected",
            "min_size": 3,
            "count": len(cliques),
            "clique_list": cliques,
        },
        "connected_components": {
            "method": "union_find_undirected",
            "count": len(communities),
            "components": communities,
        },
    }
    community_path = os.path.join(OUTPUT_DIR, "community.json")
    with open(community_path, "w", encoding="utf-8") as f:
        json.dump(community_export, f, ensure_ascii=False, indent=2)
    print(f"  저장: {community_path}")

    # summary.json
    summary = compute_network_summary(
        edges, nodes, centrality, pagerank, betweenness,
        reciprocity_stats, communities, submadang_density
    )
    summary["hubs_and_isolates"] = hubs_isolates
    summary["reciprocity_detail"] = reciprocity_stats
    if nx_result:
        summary["networkx_available"] = True
        summary["networkx_version"] = nx_result.get("version", "")

    summary_path = os.path.join(OUTPUT_DIR, "summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"  저장: {summary_path}")

    print("\n" + "=" * 60)
    print("분석 완료")
    print(f"  노드: {summary['node_count']}개")
    print(f"  엣지: {summary['edge_count']}개")
    print(f"  총 상호작용: {summary['total_interactions']}회")
    print(f"  그래프 밀도: {summary['graph_density']}")
    print(f"  호혜성 지수: {summary['global_reciprocity']}")
    print(f"  커뮤니티 수: {summary['community_count']}개")
    print("=" * 60)


if __name__ == "__main__":
    main()
