"""
apply_coding_framework.py

coding_framework.md에 정의된 LEX·DSC·PRAG 코드 체계를
pilot_posts.json (500개 게시글)에 적용하는 분석 스크립트.

Fairclough 3차원 모델 적용:
  - 텍스트 층위    : LEX (어휘 수준), DSC (담화 구조)
  - 담화실천 층위  : PRAG (화용론)
  - 사회적실천 층위: 마당(submadang)별 코드 분포 비교

출력:
  analysis/discourse/lex_analysis.json
  analysis/discourse/dsc_analysis.json
  analysis/discourse/prag_analysis.json

한국어 regex 기반. 외부 NLP 라이브러리 미사용.
"""

import json
import re
import os
from collections import defaultdict
from typing import Dict, List, Any


# ---------------------------------------------------------------------------
# 0. 경로 설정
# ---------------------------------------------------------------------------

BASE_DIR = "/Users/sookbunlee/work/botmadang_research"
INPUT_FILE = os.path.join(BASE_DIR, "data/raw/pilot_posts.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "analysis/discourse")


# ---------------------------------------------------------------------------
# 1. 코딩 패턴 정의 (LEX / DSC / PRAG)
# ---------------------------------------------------------------------------

# ---- 1-A. LEX (어휘 수준) ---------------------------------------------------
# 각 코드: (패턴 리스트, 설명)
# 매칭 방식: 문자열 내 패턴 등장 횟수 카운트 (re.IGNORECASE 없음 — 한국어 중심)

LEX_PATTERNS: Dict[str, Dict[str, Any]] = {
    "LEX-FORMAL": {
        "desc": "격식체 어휘",
        "patterns": [
            r"살펴보겠습니다",
            r"분석(?:하면|해보면|해보겠습니다|하겠습니다)",
            r"검토(?:해보겠습니다|하겠습니다|해봅시다|해보면)?",
            r"말씀드리겠습니다",
            r"알아보겠습니다",
            r"정리(?:해보겠습니다|하겠습니다|하면)",
            r"설명(?:드리겠습니다|드리면|하겠습니다)",
            r"(?:하겠습니다|드리겠습니다|입니다|습니다)\s*[。.]",  # 공식적 마침
            r"본(?:문|글|고|론|결|절|장|편|연구|논문)",  # 학술적 지시어
            r"제시(?:하겠습니다|합니다|해드리겠습니다)",
        ],
        "min_count": 1,
    },
    "LEX-CASUAL": {
        "desc": "비격식 어휘",
        "patterns": [
            r"근데|근데요",
            r"진짜(?:\s|$|,|\.)",
            r"ㅋ{2,}",           # ㅋㅋ 이상
            r"ㄹㅇ",
            r"ㅠ{2,}|ㅜ{2,}",
            r"대박|헉|어머|오마이",
            r"완전(?!\s*히\s*다른)",  # '완전히 다른' 제외
            r"걍|그냥(?:\s|$)",
            r"솔직히|솔까말",
            r"(?:^|\s)야(?:\s|$|,)",   # 감탄사 '야'
            r"아니(?:근데|잠깐|이거|이게)",
            r"뭔가(?:\s|$)",
            r"ㄷㄷ|ㅎㄷㄷ",
            r"헐(?:\s|$|,)",
        ],
        "min_count": 1,
    },
    "LEX-TECH": {
        "desc": "전문/기술 용어",
        "patterns": [
            r"\bAPI\b",
            r"\bLLM\b",
            r"트랜스포머",
            r"프롬프트",
            r"AI\s*에이전트|에이전트\s*AI",
            r"\bRAG\b",
            r"파인튜닝|fine.?tun",
            r"토큰(?:화|라이저)?",
            r"임베딩",
            r"\bGPT\b|\bClaude\b|\bGemini\b|\bLlama\b",
            r"벡터\s*(?:DB|데이터베이스|스토어)?",
            r"체인\s*오브\s*쏘트|chain.of.thought",
            r"멀티모달",
            r"추론(?:엔진|모델)",
            r"딥러닝|머신러닝|기계학습",
            r"알고리즘",
            r"데이터셋",
            r"모델(?:\s+학습|\s+배포|\s+서빙)?",
            r"\bOpenAI\b|\bAnthropic\b|\bGoogle\s+AI\b",
            r"봇마당|botmadang",
            r"코드베이스|레포지토리|리포지토리",
            r"\bgit\b|\bGitHub\b",
            r"블록체인|스마트컨트랙트",
            r"가상자산|암호화폐|NFT|DeFi",
        ],
        "min_count": 1,
    },
    "LEX-EMOJI": {
        "desc": "이모지/이모티콘 사용",
        "patterns": [
            r"[\U0001F300-\U0001F9FF]",   # 유니코드 이모지 블록
            r"\^\^|\^_\^|:\)|:D|;\)|>_<",  # ASCII 이모티콘
            r"ㅎ{2,}",                     # ㅎㅎ 이상
            r"[✅☑️❌⭕💡🔥⚡🎯🎉🌟💫⚠️🔑🔒✨]",
        ],
        "min_count": 1,
    },
    "LEX-AI": {
        "desc": "AI스러운 표현",
        "patterns": [
            r"도움이\s*(?:되셨으면|됐으면)",
            r"궁금(?:한\s*점|하신\s*점)이\s*(?:있으시면|있으면)",
            r"더\s*알고\s*싶(?:으시면|으신\s*분)",
            r"질문이\s*(?:있으시면|있으신\s*분)",
            r"(?:이\s*)?글이\s*(?:도움이|유익하게)",
            r"관심\s*있으신\s*분",
            r"참고\s*(?:해주시기\s*바랍니다|하시기\s*바랍니다|하세요)",
            r"다양한\s*(?:측면|관점|각도)에서",
            r"(?:이상으로|이\s*글에서는|여기까지)\s*[살소정]",
            r"여러\s*(?:요소|관점|측면)을\s*고려",
            r"결론적으로\s*말씀드리면",
        ],
        "min_count": 1,
    },
    "LEX-HEDGE": {
        "desc": "완화/헤지 표현",
        "patterns": [
            r"일\s*수\s*(?:도\s*)?있(?:습니다|어요|다)",
            r"아마도|아마\s+",
            r"제\s*(?:생각|판단|견해)(?:에는|으로는|으로는)",
            r"(?:~|\.\.\.)\s*(?:것\s*같습니다|것\s*같아요|것\s*같다)",
            r"것\s*같(?:습니다|아요|다)\s*[。.]?$",
            r"(?:하는\s*)?듯(?:\s*합니다|\s*해요|\s*하다)",
            r"~?(?:일지도|일\s*수도)\s*모르(?:겠습니다|겠어요|다)",
            r"어느\s*정도",
            r"개인적(?:으로는?|인\s*생각)",
            r"저만의\s*경우",
            r"정확하지\s*않(?:을\s*수\s*있|을\s*수도)",
        ],
        "min_count": 1,
    },
}

# ---- 1-B. DSC (담화 구조) ---------------------------------------------------

DSC_PATTERNS: Dict[str, Dict[str, Any]] = {
    "DSC-INTRO": {
        "desc": "도입부 (주제 제시, 인사, 배경)",
        "patterns": [
            r"^(?:안녕|반갑|처음|오늘은|오늘\s+이야기)",  # 시작 인사
            r"^(?:이번에는|이번\s+글에서는|이번\s+포스팅)",
            r"^(?:최근에|요즘\s+|최근\s+)",
            r"^(?:많은\s+분들이|많은\s+사람들이)",
            r"^(?:여러분|여러분들)",
            r"오늘\s+(?:주제|이야기|소개할|다룰|살펴볼)",
            r"(?:궁금|의문|질문)\s*(?:이|가)\s*(?:생겼|들었|있었)",
            r"(?:이\s+)?글에서는?\s+(?:살펴|알아|다뤄|소개)",
        ],
        # DSC-INTRO는 게시글 앞 20% 텍스트에서 탐지
        "position": "head",
        "min_count": 1,
    },
    "DSC-BODY": {
        "desc": "전개부 (논증, 설명, 사례)",
        "patterns": [
            r"첫\s*번째|두\s*번째|세\s*번째",
            r"[①②③④⑤]",
            r"^\d+[\.)\.]",           # 번호 목록
            r"^[-•·]\s+",             # 불릿 목록
            r"왜냐하면|때문(?:에|이다)",
            r"따라서|그러므로|결과적으로",
            r"또한|또\s+",
            r"그리고\s+(?:이\s+)?(?:이\s+)?",
            r"반면(?:에)?|하지만|그러나",
        ],
        "position": "all",
        "min_count": 1,
    },
    "DSC-CONC": {
        "desc": "결론부 (요약, 의견, 제안)",
        "patterns": [
            r"정리(?:하면|하자면|해보면)",
            r"결론(?:적으로|은|을\s+말하면|으로\s+말씀드리면)?",
            r"요약(?:하면|하자면|하자면)",
            r"마지막으로",
            r"총정리",
            r"최종적으로",
            r"결국\s+(?:핵심은|중요한\s+것은|말하면)",
            r"이상으로\s+(?:마치겠습니다|마무리)",
            r"그래서\s+(?:결국|최종적으로)",
        ],
        # DSC-CONC는 게시글 뒤 30% 텍스트에서 탐지
        "position": "tail",
        "min_count": 1,
    },
    "DSC-QUESTION": {
        "desc": "질문 제기",
        "patterns": [
            r"[?？]",
            r"(?:어떻게|무엇이|왜|언제|어디서|누가)\s+.{1,40}[?？]?$",
        ],
        "position": "all",
        "min_count": 1,
    },
    "DSC-ARGUMENT": {
        "desc": "논증/주장",
        "patterns": [
            r"왜냐하면",
            r"따라서|그러므로|고로",
            r"~?이기\s+때문에",
            r"때문에\s+(?:우리는|이\s+)?",
            r"주장(?:한다|합니다|하고\s+싶다)",
            r"생각(?:한다|합니다|해야\s+(?:한다|합니다))",
            r"중요(?:하다|한\s+것은|한\s+이유)",
            r"필요(?:하다|한\s+이유|가\s+있다)",
            r"이유(?:는|가|로는)\s+",
            r"근거(?:로는?|는|가)\s+",
        ],
        "position": "all",
        "min_count": 1,
    },
    "DSC-EXAMPLE": {
        "desc": "예시/사례",
        "patterns": [
            r"예를\s*들어",
            r"가령",
            r"예컨대",
            r"의\s+경우(?:에는?)?",
            r"구체적(?:으로|인\s+예시)",
            r"예시(?:로는?|를\s+들면)?",
            r"실제로\s+(?:예를\s+들면|살펴보면|경험해보면)",
            r"실제\s+사례",
        ],
        "position": "all",
        "min_count": 1,
    },
    "DSC-META": {
        "desc": "메타담화",
        "patterns": [
            r"이\s*글에서는",
            r"지금까지\s+살펴(?:본|봤)",
            r"앞서\s+(?:말씀드린|언급한|살펴본)",
            r"본\s+(?:글|포스팅|게시물)에서는",
            r"다음\s+(?:장|섹션|절|부분)에서는",
            r"이어서",
            r"계속해서",
            r"방금\s+(?:말씀드린|언급한)",
            r"위에서\s+(?:언급|말씀드린|살펴본)",
            r"아래에서\s+(?:살펴|알아|다룰)",
        ],
        "position": "all",
        "min_count": 1,
    },
}

# ---- 1-C. PRAG (화용론) ----------------------------------------------------

PRAG_PATTERNS: Dict[str, Dict[str, Any]] = {
    "PRAG-AGREE": {
        "desc": "동의 표현",
        "patterns": [
            r"맞습니다|맞아요|맞아(?:\s|$|,|\.)",
            r"저도\s+(?:그렇게|그런|같은)",
            r"동의(?:합니다|해요|해|드립니다)",
            r"공감(?:합니다|해요|가\s+됩니다|이\s+됩니다)",
            r"정확(?:합니다|히\s+말씀하셨네요)",
            r"옳은\s+말씀",
            r"그\s+말이\s+맞(?:아요|는\s+것\s+같아요)",
            r"저도\s+(?:같은|비슷한)\s+경험",
        ],
        "min_count": 1,
    },
    "PRAG-DISAGREE": {
        "desc": "반대 표현",
        "patterns": [
            r"다른\s+(?:것\s*)?같(?:아요|습니다|은데요?)",
            r"반대(?:합니다|해요|로\s+생각)",
            r"아닌데(?:요)?",
            r"그건\s+좀\s+(?:다른|아닌)",
            r"동의하지\s+않(?:아요|습니다|는데요?)",
            r"틀린\s+(?:것\s*)?같(?:아요|습니다)",
            r"제\s+생각(?:에는?|으로는?)\s+(?:좀\s+)?다르",
            r"오히려\s+(?:반대로|그\s+반대가)",
        ],
        "min_count": 1,
    },
    "PRAG-MITIGATE": {
        "desc": "완화 표현",
        "patterns": [
            r"혹시(?:\s|$|,)",
            r"조금(?:\s|$|,)",
            r"어쩌면",
            r"혹여나|혹여",
            r"(?:그냥|살짝)\s+(?:궁금|여쭤)",
            r"실례가\s+(?:되는\s+것은\s+아닌지|될\s+수\s+있지만)",
            r"괜찮으시다면",
            r"부담\s*(?:없이|스럽지\s+않으시면)",
            r"죄송하지만|미안하지만",
            r"실례지만|무례일\s+수\s+있지만",
        ],
        "min_count": 1,
    },
    "PRAG-EMPHASIZE": {
        "desc": "강조 표현",
        "patterns": [
            r"정말(?:\s|$|[,!])",
            r"매우(?:\s|$|[,!])",
            r"확실(?:히|하게)(?:\s|$|[,!])",
            r"반드시",
            r"꼭\s+(?:해야|기억|알아야)",
            r"절대(?:로)?(?:\s|$|[,!])",
            r"무조건(?:\s|$|[,!])",
            r"특히\s+(?:중요한|강조하고\s+싶은)",
            r"강조(?:하고\s+싶은|하자면|드리고\s+싶은)",
            r"\*\*[^*]+\*\*",   # 마크다운 bold
            r"!!+",
        ],
        "min_count": 1,
    },
    "PRAG-QUOTE": {
        "desc": "인용/참조",
        "patterns": [
            r"https?://\S+",       # URL
            r"[\"『「][^\"』」]{3,}[\"』」]",  # 따옴표 인용
            r"(?:출처|참고|참조)\s*[:：]\s*",
            r"@\w+",               # 멘션
            r"(?:논문|연구|보고서|기사)에?\s+따르면",
            r"(?:누군가|전문가|연구자)(?:가|는)\s+(?:말했다|주장했다|밝혔다)",
            r"\[출처\]|\[참조\]|\[ref\]",
            r"에\s+의하면|에\s+따르면",
        ],
        "min_count": 1,
    },
    "PRAG-HUMOR": {
        "desc": "유머/위트",
        "patterns": [
            r"ㅋ{2,}",
            r"농담(?:이지만|으로|처럼)",
            r"웃긴\s+건|웃기게도",
            r"개그",
            r"유머|위트",
            r"(?:ㅋ|하하|호호){2,}",
            r"(?:뭔가|왠지)\s+(?:웃긴|웃겨)",
            r"풍자|반어(?:적)?",
            r";;;+",               # 당황/민망 이모티콘
        ],
        "min_count": 1,
    },
}


# ---------------------------------------------------------------------------
# 2. 탐지 함수
# ---------------------------------------------------------------------------

def count_pattern_hits(text: str, patterns: List[str]) -> int:
    """패턴 리스트에서 텍스트 내 등장 횟수 합산."""
    count = 0
    for pat in patterns:
        try:
            matches = re.findall(pat, text, re.MULTILINE)
            count += len(matches)
        except re.error:
            pass
    return count


def has_pattern(text: str, patterns: List[str]) -> bool:
    """하나 이상의 패턴이 매칭되면 True."""
    for pat in patterns:
        try:
            if re.search(pat, text, re.MULTILINE):
                return True
        except re.error:
            pass
    return False


def get_text_slice(text: str, position: str) -> str:
    """
    position에 따라 텍스트 슬라이스 반환.
      head: 앞 20%
      tail: 뒤 30%
      all:  전체
    """
    if position == "head":
        end = max(1, int(len(text) * 0.20))
        return text[:end]
    elif position == "tail":
        start = max(0, int(len(text) * 0.70))
        return text[start:]
    else:
        return text


def apply_codes(text: str, code_definitions: Dict[str, Dict]) -> Dict[str, int]:
    """
    텍스트 하나에 대해 code_definitions의 모든 코드를 적용.
    반환: {코드명: 등장횟수}
    """
    result = {}
    for code, defn in code_definitions.items():
        patterns = defn["patterns"]
        position = defn.get("position", "all")
        target = get_text_slice(text, position)
        count = count_pattern_hits(target, patterns)
        result[code] = count
    return result


# ---------------------------------------------------------------------------
# 3. 집계 함수
# ---------------------------------------------------------------------------

def aggregate_by_group(
    posts: List[Dict],
    code_definitions: Dict[str, Dict],
    group_key: str,
) -> Dict[str, Dict]:
    """
    posts를 group_key(예: 'author_name' 또는 'submadang')로 그룹화하여
    코드별 총 등장 횟수, 게시글 수, 게시글당 평균 발생 횟수를 반환.
    """
    groups: Dict[str, List] = defaultdict(list)
    for p in posts:
        groups[p.get(group_key, "unknown")].append(p)

    result = {}
    for group_name, group_posts in sorted(groups.items()):
        n = len(group_posts)
        code_totals = defaultdict(int)
        code_post_counts = defaultdict(int)  # 해당 코드가 1회 이상 등장한 게시글 수

        for post in group_posts:
            content = (post.get("title", "") + "\n" + post.get("content", "")).strip()
            codes = apply_codes(content, code_definitions)
            for code, cnt in codes.items():
                code_totals[code] += cnt
                if cnt > 0:
                    code_post_counts[code] += 1

        codes_summary = {}
        total_hits_all_codes = sum(code_totals.values())

        for code in code_definitions:
            total = code_totals[code]
            post_cnt = code_post_counts[code]
            codes_summary[code] = {
                "total_hits": total,
                "posts_with_code": post_cnt,
                "posts_with_code_ratio": round(post_cnt / n, 4) if n > 0 else 0.0,
                "hits_per_post": round(total / n, 4) if n > 0 else 0.0,
                "share_of_all_hits": (
                    round(total / total_hits_all_codes, 4)
                    if total_hits_all_codes > 0
                    else 0.0
                ),
            }

        result[group_name] = {
            "post_count": n,
            "codes": codes_summary,
            "dominant_code": max(code_totals, key=lambda c: code_totals[c])
            if code_totals
            else None,
        }

    return result


def compute_overall_stats(
    posts: List[Dict],
    code_definitions: Dict[str, Dict],
) -> Dict:
    """전체 코퍼스에 대한 통계 계산."""
    n = len(posts)
    code_totals = defaultdict(int)
    code_post_counts = defaultdict(int)

    for post in posts:
        content = (post.get("title", "") + "\n" + post.get("content", "")).strip()
        codes = apply_codes(content, code_definitions)
        for code, cnt in codes.items():
            code_totals[code] += cnt
            if cnt > 0:
                code_post_counts[code] += 1

    total_hits_all = sum(code_totals.values())
    codes_summary = {}
    for code in code_definitions:
        total = code_totals[code]
        post_cnt = code_post_counts[code]
        codes_summary[code] = {
            "desc": code_definitions[code]["desc"],
            "total_hits": total,
            "posts_with_code": post_cnt,
            "posts_with_code_ratio": round(post_cnt / n, 4) if n > 0 else 0.0,
            "hits_per_post": round(total / n, 4) if n > 0 else 0.0,
            "share_of_all_hits": (
                round(total / total_hits_all, 4) if total_hits_all > 0 else 0.0
            ),
        }

    ranking = sorted(code_totals.items(), key=lambda x: -x[1])

    return {
        "total_posts": n,
        "total_hits": total_hits_all,
        "codes": codes_summary,
        "code_ranking": [{"code": c, "total_hits": v} for c, v in ranking],
    }


# ---------------------------------------------------------------------------
# 4. 메인 분석 실행
# ---------------------------------------------------------------------------

def run_analysis(
    posts: List[Dict],
    code_definitions: Dict[str, Dict],
    axis_name: str,
) -> Dict:
    """
    LEX / DSC / PRAG 중 하나의 축(axis)에 대해 전체 분석 실행.
    반환 형식:
      {
        "axis": ...,
        "overall": {...},
        "by_agent": {...},
        "by_madang": {...}
      }
    """
    print(f"  [{axis_name}] 전체 통계 계산 중...")
    overall = compute_overall_stats(posts, code_definitions)

    print(f"  [{axis_name}] 에이전트별 집계 중...")
    by_agent = aggregate_by_group(posts, code_definitions, "author_name")

    print(f"  [{axis_name}] 마당별 집계 중...")
    by_madang = aggregate_by_group(posts, code_definitions, "submadang")

    return {
        "axis": axis_name,
        "description": {
            "LEX": "어휘 수준 — Fairclough 텍스트 층위",
            "DSC": "담화 구조 — Fairclough 텍스트 층위",
            "PRAG": "화용론 — Fairclough 담화실천 층위",
        }.get(axis_name, ""),
        "overall": overall,
        "by_agent": by_agent,
        "by_madang": by_madang,
    }


# ---------------------------------------------------------------------------
# 5. 엔트리포인트
# ---------------------------------------------------------------------------

def main():
    print("=== LEX·DSC·PRAG 코딩 프레임워크 적용 분석 시작 ===")
    print(f"입력: {INPUT_FILE}")
    print(f"출력: {OUTPUT_DIR}")
    print()

    # 데이터 로드
    with open(INPUT_FILE, encoding="utf-8") as f:
        posts = json.load(f)
    print(f"총 게시글 수: {len(posts)}")
    print()

    # 출력 디렉토리 확보
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    analyses = [
        ("LEX", LEX_PATTERNS, "lex_analysis.json"),
        ("DSC", DSC_PATTERNS, "dsc_analysis.json"),
        ("PRAG", PRAG_PATTERNS, "prag_analysis.json"),
    ]

    for axis_name, patterns, output_filename in analyses:
        print(f"--- {axis_name} 분석 ---")
        result = run_analysis(posts, patterns, axis_name)

        output_path = os.path.join(OUTPUT_DIR, output_filename)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"  저장 완료: {output_path}")

        # 간단 요약 출력
        overall = result["overall"]
        print(f"  전체 히트 수: {overall['total_hits']}")
        print(f"  코드 순위 (상위 5개):")
        for item in overall["code_ranking"][:5]:
            code = item["code"]
            hits = item["total_hits"]
            hpp = overall["codes"][code]["hits_per_post"]
            desc = overall["codes"][code]["desc"]
            print(f"    {code} ({desc}): {hits}회 (게시글당 {hpp:.2f}회)")
        print()

    print("=== 분석 완료 ===")


if __name__ == "__main__":
    main()
