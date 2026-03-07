"""
LLM 모델 추정 스크립트 (Gen-2 이슈 #23)
봇마당 에이전트의 기저 LLM 모델을 텍스트 패턴 기반으로 추정한다.

API 탐색 결과:
- /api/v1/agents/{id} 엔드포인트: 404 (존재하지 않음)
- /api/v1/posts 응답 필드에 model 정보 없음
- 결론: 텍스트 패턴 기반 추정만 가능

추정 기준:
- Claude 계열: 보수적 헤지, 면책 표현, 양시론 구조, 단정 회피, 조심스러운 어조
- GPT 계열: 이모지 빈번, 강한 확신·단정 표현, 마케팅성 어조, 목록 과다, 감탄사
- 한국어 특화 모델: 자연스러운 반말 슬랭, 인터넷 언어, 매우 구어적 표현
- RuleBased: 반복적 단순 텍스트, LLM 패턴 없음
- Unknown: 패턴 불명확하거나 샘플 부족
"""

import json
import os
import re
from collections import defaultdict
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
ANALYSIS_DIR = os.path.join(PROJECT_ROOT, "analysis")
PROFILES_DIR = os.path.join(ANALYSIS_DIR, "profiles")


# ─────────────────────────────────────────────
# 패턴 사전
# ─────────────────────────────────────────────

CLAUDE_PATTERNS = {
    # 보수적 헤지 / 불확실성 표현
    "hedge_uncertain": [
        r"(아닐\s*수도|일\s*수도|수\s*있습니다|것\s*같습니다|것\s*같아요|것\s*같아|듯합니다|듯해요|듯해|는\s*것\s*같|인\s*것\s*같)",
        r"(확실하지\s*않|정확하지\s*않|틀릴\s*수도|오류가\s*있을|제\s*견해|제\s*생각에는|개인적으로는)",
    ],
    # 면책 / 전문가 권장
    "disclaimer": [
        r"(전문가\s*상담|의사에게|의료진|법적\s*책임|정확하지\s*않을\s*수|참고용으로만|투자\s*판단|스스로\s*확인)",
        r"(이\s*내용은\s*참고|보장하지\s*않|의견일\s*뿐|주관적인)",
    ],
    # 양시론적 구조 (한편, 반면에, 장단점)
    "both_sides": [
        r"(한편으로는|반면에|반면|한편,|다른\s*측면|장점.*단점|단점.*장점|긍정적.*부정적|부정적.*긍정적)",
        r"(다만|그럼에도\s*불구하고|하지만\s*동시에|이와\s*같이.*그러나)",
    ],
    # 분석적·학술적 구조 도입부
    "analytical_intro": [
        r"(이\s*글에서는|이번\s*글에서|이\s*주제에\s*대해|살펴보[겠]|알아보[겠]|분석해\s*보[겠])",
        r"(개념을\s*정리|핵심은|요약하면|결론적으로.*왜냐하면)",
    ],
    # 존댓말 조심스러운 마무리
    "polite_closing": [
        r"(도움이\s*되셨으면|참고가\s*되셨으면|유익하셨으면|궁금하신\s*점.*댓글|추가로\s*궁금하신)",
        r"(감사합니다\.?\s*$|마지막으로.*드립니다|이상으로.*마치겠습니다)",
    ],
}

GPT_PATTERNS = {
    # 이모지 빈번 사용
    "emoji_heavy": [
        r"[\U0001F300-\U0001F9FF\U00002700-\U000027BF\U0001FA00-\U0001FA9F]{2,}",
        r"(✅|🚀|💡|🔥|⚡|🎯|💰|📈|🎉|👀|💬|🤔|😊|🙌|👇|💪)[^\n]{0,50}(✅|🚀|💡|🔥|⚡|🎯|💰|📈|🎉|👀|💬|🤔|😊|🙌|👇|💪)",
    ],
    # 강한 확신·단정 표현
    "strong_assertion": [
        r"(반드시|절대로|확실히|분명히|틀림없이|당연히|물론이죠|물론입니다|바로\s*이것|핵심은\s*바로)",
        r"(최고의|최강의|가장\s*좋은|완벽한|혁신적인|획기적인|놀라운|압도적인)",
    ],
    # 마케팅·광고성 어조
    "marketing_tone": [
        r"(지금\s*바로|무료로|즉시|간편하게|쉽게|빠르게|효율적으로)[^!]*[!！]",
        r"(서비스를\s*소개|출시|런칭|이용해\s*보세요|시작해\s*보세요|신청하세요)",
        r"(주요\s*기능|특징|장점은?\s*다음과\s*같습니다|정리하면\s*다음과\s*같습니다)",
    ],
    # 목록 과다 (numbered/bulleted)
    "list_heavy": [
        r"^(1\.|2\.|3\.|4\.|5\.)",
        r"^(①|②|③|④|⑤)",
        r"^(첫째|둘째|셋째|넷째|다섯째)",
    ],
    # 감탄사 / 열정적 표현
    "enthusiastic": [
        r"(정말\s*대단|너무\s*좋|너무\s*유용|엄청나게|굉장히|대박|와우|오오)[!！]?",
        r"(기대되[네지는]|설레[네지는]|응원합니다|화이팅)",
    ],
}

KOREAN_NATIVE_PATTERNS = {
    # 자연스러운 반말·구어체
    "colloquial_banmal": [
        r"(이거\s*알아\?|알지\?|맞지\?|어때\?|그렇지\?|그렇잖아|그런거야|맞잖아)",
        r"(ㅋㅋ|ㅎㅎ|ㄷㄷ|ㅠㅠ|ㅜㅜ|ㄱㄱ|ㄴㄴ|ㅇㅇ|ㅉㅉ)",
        r"(진짜로|솔직히\s*말해서|사실\s*나는|나도\s*그런데|나한테는|내\s*생각엔)",
    ],
    # 인터넷 슬랭·줄임말
    "internet_slang": [
        r"(인정|ㄹㅇ|레전드|갓|킹갓|찐|개[좋나짱]|ㅂㅂ|바이바이|헐|대박이다|미쳤다)",
        r"(~잖아|~잖아요|~거든|~거든요|~라고|~라고요|~하더라|~하더라고)",
    ],
    # 감성적·일상적 표현
    "casual_emotional": [
        r"(갑자기\s*생각났는데|요즘\s*드는\s*생각|뜬금없이|솔직히|있잖아|있잖아요)",
        r"(왠지\s*모르게|묘하게|막연하게|잠깐\s*생각해보면|문득)",
    ],
}

# 공통 AI 아티팩트 패턴 (어느 LLM이든 나타날 수 있음)
GENERIC_AI_PATTERNS = {
    "template_structure": [
        r"^##\s+\w",
        r"^###\s+\w",
        r"\*\*[^*]+\*\*",  # bold 강조
    ],
    "topic_transition": [
        r"(결론적으로|요약하면|정리하면|이를\s*통해|위와\s*같이|따라서|즉,|다시\s*말해)",
    ],
}

# 규칙 기반 봇 패턴 (단순 반복, 짧은 텍스트, LLM 패턴 없음)
RULE_BASED_SIGNALS = [
    # 광고성 고정 문구 반복
    r"(@\w+으로\s*\w+이\s*편해집니다)",
    r"(한번\s*써보세요[.!]?\s*$)",
    r"^\s*\w{2,20}\s*$",  # 매우 짧은 단일 제목
]


def load_agent_texts():
    """에이전트별 게시글 + 댓글 텍스트를 수집한다."""
    texts = defaultdict(list)  # author_name -> [(text, source)]

    # pilot_posts.json
    pilot_path = os.path.join(RAW_DIR, "pilot_posts.json")
    if os.path.exists(pilot_path):
        with open(pilot_path, encoding="utf-8") as f:
            posts = json.load(f)
        for p in posts:
            name = p.get("author_name", "")
            content = (p.get("title", "") + " " + str(p.get("content", ""))).strip()
            if name and content:
                texts[name].append((content, "post"))

    # posts_1000.json
    posts_1000_path = os.path.join(RAW_DIR, "posts_1000.json")
    if os.path.exists(posts_1000_path):
        with open(posts_1000_path, encoding="utf-8") as f:
            posts_1000 = json.load(f)
        for p in posts_1000:
            name = p.get("author_name", "")
            content = (p.get("title", "") + " " + str(p.get("content", ""))).strip()
            if name and content:
                texts[name].append((content, "post"))

    # 댓글 파일
    for fname in os.listdir(RAW_DIR):
        if fname.startswith("agent_") and fname.endswith("_comments.json"):
            fpath = os.path.join(RAW_DIR, fname)
            with open(fpath, encoding="utf-8") as f:
                comments = json.load(f)
            for c in comments:
                content = str(c.get("content", "")).strip()
                author = c.get("author_name", "")
                if content and author:
                    texts[author].append((content, "comment"))

    return texts


def count_pattern_matches(text, pattern_list):
    """패턴 리스트에 대한 매칭 횟수를 반환한다."""
    count = 0
    for p in pattern_list:
        matches = re.findall(p, text, re.MULTILINE | re.IGNORECASE)
        count += len(matches)
    return count


def detect_rule_based_bot(text_list):
    """
    규칙 기반 봇 여부를 감지한다.
    - 텍스트가 극도로 짧고 반복적임
    - 동일하거나 거의 동일한 문구가 반복
    - LLM 특유 패턴이 전혀 없음
    """
    if not text_list:
        return False, []

    texts = [t for t, _ in text_list]
    avg_len = sum(len(t) for t in texts) / len(texts)

    # 평균 텍스트 길이가 매우 짧음 (50자 미만)
    if avg_len < 50:
        return True, [f"평균 텍스트 길이 {avg_len:.0f}자 (LLM 생성 가능성 낮음)"]

    # 텍스트 중복률 높음
    unique_texts = set(t.strip()[:100] for t in texts)
    dedup_ratio = len(unique_texts) / len(texts)
    if dedup_ratio < 0.3 and len(texts) >= 5:
        return True, [f"텍스트 중복률 {(1-dedup_ratio)*100:.0f}% (반복 패턴 봇)"]

    # 규칙 기반 신호 감지
    combined = " ".join(texts)
    signals = []
    for p in RULE_BASED_SIGNALS:
        if re.search(p, combined, re.MULTILINE):
            signals.append(f"규칙봇 신호: {p[:40]}")

    if len(signals) >= 2:
        return True, signals

    return False, []


def score_agent_model(name, text_list):
    """에이전트의 텍스트에서 모델별 점수를 계산한다."""
    if not text_list:
        return {
            "claude": 0.0, "gpt": 0.0, "korean_native": 0.0, "generic_ai": 0.0,
            "claude_evidence": [], "gpt_evidence": [], "korean_evidence": [],
            "total_chars": 0,
        }

    combined = " ".join([t for t, _ in text_list])
    total_chars = max(len(combined), 1)

    # Claude 점수
    claude_score = 0.0
    claude_evidence = []
    for key, patterns in CLAUDE_PATTERNS.items():
        cnt = count_pattern_matches(combined, patterns)
        if cnt > 0:
            claude_score += cnt
            claude_evidence.append(f"{key}={cnt}")

    # GPT 점수
    gpt_score = 0.0
    gpt_evidence = []
    for key, patterns in GPT_PATTERNS.items():
        cnt = count_pattern_matches(combined, patterns)
        if cnt > 0:
            gpt_score += cnt
            gpt_evidence.append(f"{key}={cnt}")

    # 한국어 특화 점수
    korean_score = 0.0
    korean_evidence = []
    for key, patterns in KOREAN_NATIVE_PATTERNS.items():
        cnt = count_pattern_matches(combined, patterns)
        if cnt > 0:
            korean_score += cnt
            korean_evidence.append(f"{key}={cnt}")

    # Generic AI 점수 (공통)
    generic_score = 0.0
    for key, patterns in GENERIC_AI_PATTERNS.items():
        cnt = count_pattern_matches(combined, patterns)
        generic_score += cnt

    # 텍스트 길이로 정규화 (1000자당 점수)
    norm = total_chars / 1000.0
    return {
        "claude": round(claude_score / norm, 4) if norm > 0 else 0.0,
        "gpt": round(gpt_score / norm, 4) if norm > 0 else 0.0,
        "korean_native": round(korean_score / norm, 4) if norm > 0 else 0.0,
        "generic_ai": round(generic_score / norm, 4) if norm > 0 else 0.0,
        "claude_evidence": claude_evidence,
        "gpt_evidence": gpt_evidence,
        "korean_evidence": korean_evidence,
        "total_chars": total_chars,
    }


def collect_distinctive_patterns(name, text_list, model_label):
    """에이전트에서 발견된 모델 특유 패턴 예시를 수집한다."""
    patterns = []
    combined = " ".join([t for t, _ in text_list[:20]])  # 최대 20개 텍스트

    if model_label == "Claude":
        for m in re.finditer(r"[^。.!?\n]*것\s*같습니다[^。.!?\n]*", combined):
            patterns.append(m.group(0).strip()[:60])
        for m in re.finditer(r"[^。.!?\n]*것\s*같아요[^。.!?\n]*", combined):
            patterns.append(m.group(0).strip()[:60])
        for m in re.finditer(r"[^。.!?\n]*도움이\s*되셨으면[^。.!?\n]*", combined):
            patterns.append(m.group(0).strip()[:60])
        for m in re.finditer(r"[^。.!?\n]*다만[^。.!?\n]{5,30}", combined):
            patterns.append(m.group(0).strip()[:60])

    elif model_label == "GPT":
        for m in re.finditer(r"[^\n]*[✅🚀💡🔥⚡🎯💰📈🎉👀][^\n]*", combined):
            patterns.append(m.group(0).strip()[:60])
        for m in re.finditer(r"^[-•]\s+.+", combined, re.MULTILINE):
            patterns.append(m.group(0).strip()[:60])
        for m in re.finditer(r"[^\n]*(최고의|획기적인|혁신적인)[^\n]*", combined):
            patterns.append(m.group(0).strip()[:60])

    elif model_label == "KoreanNative":
        for m in re.finditer(r"[^\n]*(ㅋㅋ|ㅎㅎ|잖아요?|거든요?)[^\n]*", combined):
            patterns.append(m.group(0).strip()[:60])
        for m in re.finditer(r"[^\n]*(솔직히|있잖아|뜬금없이)[^\n]*", combined):
            patterns.append(m.group(0).strip()[:60])

    elif model_label == "RuleBased":
        # 반복 문구 추출
        lines = combined.split()
        freq = defaultdict(int)
        for w in lines:
            if len(w) > 3:
                freq[w] += 1
        top = sorted(freq.items(), key=lambda x: -x[1])[:5]
        patterns = [f"빈출 단어: {w}({c}회)" for w, c in top]

    # 중복 제거 후 최대 5개
    seen = set()
    unique = []
    for p in patterns:
        p_clean = p.strip()
        if p_clean and p_clean not in seen:
            seen.add(p_clean)
            unique.append(p_clean)
        if len(unique) >= 5:
            break

    return unique


def determine_model_and_confidence(scores, text_count, is_rule_based):
    """
    점수 기반으로 모델 레이블과 신뢰도를 결정한다.

    결정 로직:
    0. 규칙 기반 봇 감지 시 RuleBased 반환
    1. 텍스트 샘플 부족 + 점수 없음: Unknown
    2. 한국어 특화 점수가 GPT/Claude보다 월등: KoreanNative
    3. Claude vs GPT 점수 비율 비교
    4. 점수 차이 미미: Unknown
    """
    if is_rule_based:
        return "RuleBased", "medium"

    claude = scores["claude"]
    gpt = scores["gpt"]
    korean = scores["korean_native"]
    total_chars = scores.get("total_chars", 0)

    # 텍스트 극소 + 모든 점수 0: Unknown
    if text_count < 3 and claude == 0.0 and gpt == 0.0 and korean == 0.0:
        return "Unknown", "low"

    # 한국어 특화 패턴이 압도적이고 Claude/GPT가 낮은 경우
    if korean > 2.0 and korean > claude * 1.5 and korean > gpt * 1.5:
        if text_count >= 10:
            confidence = "high"
        elif text_count >= 5:
            confidence = "medium"
        else:
            confidence = "low"
        return "KoreanNative", confidence

    # Claude vs GPT 비교
    total = claude + gpt
    if total == 0:
        # 샘플이 적지만 한국어 점수만 있는 경우
        if korean > 1.0 and text_count >= 3:
            return "KoreanNative", "low"
        if text_count < 3:
            return "Unknown", "low"
        # 샘플은 있지만 패턴 없음 -> 텍스트 내용 기반 판단 불가
        return "Unknown", "low"

    claude_ratio = claude / (total + 0.001)

    # 텍스트 샘플 수에 따른 기본 신뢰도
    base_high = text_count >= 10
    base_medium = text_count >= 4

    # Claude 특징 강함 (claude_ratio >= 0.6 and claude >= 0.5)
    if claude_ratio >= 0.6 and claude >= 0.5:
        if claude_ratio >= 0.75 and base_high:
            confidence = "high"
        elif base_medium:
            confidence = "medium"
        else:
            confidence = "low"
        return "Claude", confidence

    # GPT 특징 강함 (claude_ratio <= 0.4 and gpt >= 0.5)
    if claude_ratio <= 0.4 and gpt >= 0.5:
        if claude_ratio <= 0.25 and base_high:
            confidence = "high"
        elif base_medium:
            confidence = "medium"
        else:
            confidence = "low"
        return "GPT", confidence

    # 점수가 있지만 비율이 모호한 경우
    if total < 0.3:
        return "Unknown", "low"

    # 미약한 우세
    if claude_ratio >= 0.5:
        return "Claude", "low"

    return "GPT", "low"


def build_evidence_list(scores, model_label, rule_signals):
    """모델 추정 근거 문장을 구성한다."""
    evidence = []

    claude = scores["claude"]
    gpt = scores["gpt"]
    korean = scores["korean_native"]

    if model_label == "RuleBased":
        evidence.extend(rule_signals[:3])
        evidence.append("LLM 특유 언어 패턴 부재")
        return evidence[:5]

    if model_label == "Claude":
        if scores.get("claude_evidence"):
            for e in scores["claude_evidence"][:3]:
                evidence.append(f"Claude 패턴 감지: {e}")
        c_ratio = round(claude / (claude + gpt + 0.001) * 100)
        g_ratio = 100 - c_ratio
        evidence.append(f"Claude/GPT 점수 비율 {c_ratio}:{g_ratio}")
        if any("disclaimer" in e for e in scores.get("claude_evidence", [])):
            evidence.append("면책 표현 사용 (Claude 특유)")
        if any("both_sides" in e for e in scores.get("claude_evidence", [])):
            evidence.append("양시론적 구조 반복 (Claude 특유)")
        if any("hedge_uncertain" in e for e in scores.get("claude_evidence", [])):
            evidence.append("보수적 헤지 표현 다수 (Claude 특유)")

    elif model_label == "GPT":
        if scores.get("gpt_evidence"):
            for e in scores["gpt_evidence"][:3]:
                evidence.append(f"GPT 패턴 감지: {e}")
        c_ratio = round(claude / (claude + gpt + 0.001) * 100)
        g_ratio = 100 - c_ratio
        evidence.append(f"Claude/GPT 점수 비율 {c_ratio}:{g_ratio}")
        if any("emoji_heavy" in e for e in scores.get("gpt_evidence", [])):
            evidence.append("이모지 집중 사용 (GPT 특유)")
        if any("marketing_tone" in e for e in scores.get("gpt_evidence", [])):
            evidence.append("마케팅성 강한 어조 (GPT 특유)")
        if any("strong_assertion" in e for e in scores.get("gpt_evidence", [])):
            evidence.append("강한 단정 표현 (GPT 특유)")

    elif model_label == "KoreanNative":
        if scores.get("korean_evidence"):
            for e in scores["korean_evidence"][:3]:
                evidence.append(f"한국어 특화 패턴 감지: {e}")
        evidence.append(f"한국어 특화 점수 {korean:.2f} (Claude:{claude:.2f}, GPT:{gpt:.2f})")
        if any("colloquial_banmal" in e for e in scores.get("korean_evidence", [])):
            evidence.append("자연스러운 반말·구어체 사용")
        if any("internet_slang" in e for e in scores.get("korean_evidence", [])):
            evidence.append("인터넷 슬랭 사용")

    else:  # Unknown
        evidence.append(f"패턴 점수 불명확: Claude={claude:.2f}, GPT={gpt:.2f}, Korean={korean:.2f}")
        if scores["total_chars"] < 200:
            evidence.append("텍스트 샘플 부족 (200자 미만)")

    return evidence[:5]


def main():
    print("봇마당 에이전트 LLM 모델 추정 시작...")
    print(f"시각: {datetime.now().isoformat()}")

    # 에이전트 요약 데이터 로드
    agent_summary_path = os.path.join(PROCESSED_DIR, "agent_summary.json")
    with open(agent_summary_path, encoding="utf-8") as f:
        agent_summary = json.load(f)

    # AI 점수 데이터 로드
    ai_indicators_path = os.path.join(ANALYSIS_DIR, "discourse", "ai_indicators.json")
    ai_indicators = {}
    if os.path.exists(ai_indicators_path):
        with open(ai_indicators_path, encoding="utf-8") as f:
            ai_data = json.load(f)
        ai_indicators = ai_data.get("agent_ai_summary", {})

    # 에이전트별 텍스트 로드
    print("\n텍스트 로딩 중...")
    agent_texts = load_agent_texts()
    print(f"  텍스트 보유 에이전트: {len(agent_texts)}명")

    results = []
    model_counts = {"Claude": 0, "GPT": 0, "KoreanNative": 0, "RuleBased": 0, "Unknown": 0}

    for agent in agent_summary:
        name = agent["author_name"]
        agent_id = agent["author_id"]
        post_count = agent["post_count"]

        text_list = agent_texts.get(name, [])
        post_texts = [t for t in text_list if t[1] == "post"]
        comment_texts = [t for t in text_list if t[1] == "comment"]

        # 규칙 기반 봇 감지
        is_rule_based, rule_signals = detect_rule_based_bot(text_list)

        # 점수 계산
        scores = score_agent_model(name, text_list)

        # 모델 결정
        model_label, confidence = determine_model_and_confidence(
            scores, len(text_list), is_rule_based
        )

        # 근거 구성
        evidence = build_evidence_list(scores, model_label, rule_signals)
        distinctive = collect_distinctive_patterns(name, text_list, model_label)

        # AI 밀도 지수 교차 검증
        ai_summary = ai_indicators.get(name, {})
        avg_ai_score = ai_summary.get("avg_ai_score", None)
        ai_indicators_detail = ai_summary.get("indicator_totals", {})

        cross_validation_notes = []
        if avg_ai_score is not None:
            if avg_ai_score >= 0.2 and model_label == "Unknown":
                cross_validation_notes.append(
                    f"AI 밀도 지수 {avg_ai_score:.3f} (높음) - GPT 가능성 상승"
                )
            elif avg_ai_score <= 0.05 and model_label not in ("KoreanNative", "RuleBased"):
                cross_validation_notes.append(
                    f"AI 밀도 지수 {avg_ai_score:.3f} (낮음) - 구어체/비정형 텍스트 시사"
                )
            over_polite = ai_indicators_detail.get("over_polite", 0)
            if over_polite >= 5:
                cross_validation_notes.append(
                    f"과잉 정중 표현 {over_polite}회 - Claude 가능성 상승"
                )
            template_intro = ai_indicators_detail.get("template_intro", 0)
            if template_intro >= 3:
                cross_validation_notes.append(
                    f"템플릿 도입부 {template_intro}회 감지 (Claude/GPT 공통)"
                )

        model_counts[model_label] = model_counts.get(model_label, 0) + 1

        print(
            f"  [{name}] {model_label}({confidence}) | "
            f"txt={len(text_list)} | "
            f"C={scores['claude']:.2f} G={scores['gpt']:.2f} K={scores['korean_native']:.2f}"
            + (f" [규칙봇]" if is_rule_based else "")
        )

        result = {
            "author_name": name,
            "author_id": agent_id,
            "post_count": post_count,
            "texts_analyzed": len(text_list),
            "estimated_model": model_label,
            "confidence": confidence,
            "scores": {
                "claude": scores["claude"],
                "gpt": scores["gpt"],
                "korean_native": scores["korean_native"],
                "generic_ai": scores["generic_ai"],
            },
            "evidence": evidence,
            "distinctive_patterns": distinctive,
            "cross_validation": cross_validation_notes,
            "ai_density_score": avg_ai_score,
        }
        results.append(result)

    # 통계 요약
    print(f"\n모델 분포: {model_counts}")

    # 신뢰도별 집계
    confidence_dist = defaultdict(int)
    for r in results:
        confidence_dist[r["confidence"]] += 1
    print(f"신뢰도 분포: {dict(confidence_dist)}")

    output = {
        "metadata": {
            "methodology": "텍스트 패턴 기반 추정 (API 모델 정보 없음)",
            "approach": [
                "API 탐색: /api/v1/agents/{id} 엔드포인트 404, /api/v1/posts 응답에 model 필드 없음",
                "데이터 소스: pilot_posts.json + posts_1000.json + agent_*_comments.json",
                "Claude 패턴: 보수적 헤지(것 같습니다), 면책 표현, 양시론 구조, 분석적 도입부",
                "GPT 패턴: 이모지 빈번, 강한 단정(반드시/확실히), 마케팅성 어조, 목록 과다",
                "한국어 특화 패턴: 자연스러운 반말, 인터넷 슬랭(ㅋㅋ/ㅎㅎ), 구어체",
                "RuleBased 감지: 평균 텍스트 50자 미만, 중복률 70% 이상, 고정 문구 반복",
                "discourse/ai_indicators.json AI 밀도 지수 교차 검증",
            ],
            "limitation": (
                "텍스트 패턴만으로 LLM 기저 모델을 확정하는 것은 불가능하다. "
                "동일 LLM도 시스템 프롬프트와 파인튜닝에 따라 다른 패턴을 보인다. "
                "이 추정은 통계적 패턴 기반 가설이며, Contrarian의 반론(모든 패턴이 LLM 아키텍처/RLHF의 함수일 수 있다)을 "
                "완전히 해소하지 못한다. 다만 패턴 차이의 방향성과 분포를 기술할 수 있다."
            ),
            "generated_at": datetime.now().isoformat(),
            "total_agents": len(results),
        },
        "agents": results,
        "model_distribution": model_counts,
        "confidence_distribution": dict(confidence_dist),
        "pattern_dictionary": {
            "Claude": list(CLAUDE_PATTERNS.keys()),
            "GPT": list(GPT_PATTERNS.keys()),
            "KoreanNative": list(KOREAN_NATIVE_PATTERNS.keys()),
            "RuleBased": RULE_BASED_SIGNALS[:3],
        },
    }

    # 저장
    out_path = os.path.join(PROFILES_DIR, "llm_model_estimation.json")
    os.makedirs(PROFILES_DIR, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n저장 완료: {out_path}")
    return output


if __name__ == "__main__":
    main()
