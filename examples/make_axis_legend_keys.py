"""Generate aiOptimizer_axis_legend_keys.csv — 4분면 차트 축 범례/툴팁 신규 키 배치.

- 소스: Figma node 1435-203214 "축 범례 추가 및 툴팁 안내" (AI 옵티마이저 4분면 CEP 매트릭스).
  TO-BE: 각 축에 대한 설명(부제) 추가 + i 아이콘 호버 시 상세 툴팁 노출.
- 베이스라인: hubble_ko/ja/en JSON. 아래 6개 키는 모두 사전에 미존재(전수 확인).
- 기존 패턴 미러링:
  - 축 chip 라벨(X축/Y축) → 공용 label 네임스페이스.
  - 축 부제(점수 라벨) → 기존 userInterest*/aiCallScore* 스템 + ScoreLabel.
  - 축 툴팁(상세 설명) → 전용 tooltip 루트 네임스페이스(206개 기존 키 컨벤션).
- 출력은 aiOptimizer_sheet.csv 와 동일한 34열 헤더를 미러링 (검수 전용).
"""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "aiOptimizer_sheet.csv"   # 헤더(34열) 미러링용
OUT = ROOT / "aiOptimizer_axis_legend_keys.csv"
TODAY = "2026-06-18"

USER_INTEREST_TOOLTIP_KR = (
    "CEP와 같은 맥락의 연관 키워드들의 월 검색량을 모두 합산한 값입니다.\n"
    "프로젝트 내에서 검색량이 가장 큰 CEP를 100점, 가장 작은 CEP를 0점으로 줄 세운 상대 점수입니다.\n\n"
    "점수가 높을수록, 이 프로젝트 안에서 사람들이 더 많이 검색하는 상황입니다."
)
USER_INTEREST_TOOLTIP_JP = (
    "CEPと同じ文脈の関連キーワードの月間検索量をすべて合算した値です。\n"
    "プロジェクト内で検索量が最も多いCEPを100点、最も少ないCEPを0点として並べた相対スコアです。\n\n"
    "スコアが高いほど、このプロジェクト内で人々がより多く検索している状況を示します。"
)
USER_INTEREST_TOOLTIP_US = (
    "The sum of the monthly search volumes of all related keywords that share the same context as the CEP.\n"
    "A relative score that ranks the CEP with the highest search volume in the project as 100 and the lowest as 0.\n\n"
    "The higher the score, the more people are searching for it within this project."
)

AI_CALL_TOOLTIP_KR = (
    "CEP를 AI에 질의했을 때의 답변을 분석해, 두 점수를 합산한 값입니다. (예: 언급 40 + 인용 50 = 90점)\n"
    "・ 브랜드 언급 최대 50점 — 답변에 우리 브랜드가 얼마나 비중 있게 등장하는가\n"
    "・ 콘텐츠 인용 최대 50점 — 우리 페이지(URL)가 출처로 인용되는가\n\n"
    "점수가 높을수록, AI가 우리 브랜드를 더 잘 호출합니다."
)
AI_CALL_TOOLTIP_JP = (
    "CEPをAIに質問した際の回答を分析し、2つのスコアを合算した値です。（例：言及40 + 引用50 = 90点）\n"
    "・ブランド言及 最大50点 — 回答に自社ブランドがどれだけ比重高く登場するか\n"
    "・コンテンツ引用 最大50点 — 自社ページ（URL）が出典として引用されるか\n\n"
    "スコアが高いほど、AIが自社ブランドをより多く呼び出します。"
)
AI_CALL_TOOLTIP_US = (
    "A value that analyzes the AI's answer to a CEP query and sums two scores. (e.g., Mentions 40 + Citations 50 = 90 points)\n"
    "・Brand Mentions, up to 50 pts — how prominently your brand appears in the answer\n"
    "・Content Citations, up to 50 pts — whether your page (URL) is cited as a source\n\n"
    "The higher the score, the better AI calls up your brand."
)

# ---------------------------------------------------------------------------
# 신규 키 (NEW). (위치2, key1, key2, KR, JP, US, 메모)
# ---------------------------------------------------------------------------
NEW_ROWS = [
    ("4분면 차트", "label", "xAxis",
     "X축", "X軸", "X-axis",
     "4분면 차트 X축 chip 라벨. 공용 label 네임스페이스. node 1435-203214."),
    ("4분면 차트", "label", "yAxis",
     "Y축", "Y軸", "Y-axis",
     "4분면 차트 Y축 chip 라벨. 공용 label 네임스페이스. node 1435-203214."),
    ("4분면 차트", "aiOptimizer", "userInterestScoreLabel",
     "연관 키워드 검색량 점수 (0–100)",
     "関連キーワード検索量スコア（0〜100）",
     "Related Keyword Search Volume Score (0–100)",
     "X축 부제(점수 설명). axisUserInterest('CEP 관심도 →')/userInterestTitle 축의 점수 라벨."),
    ("4분면 차트", "aiOptimizer", "aiCallScoreLabel",
     "AI 응답 기반 브랜드 노출 점수 (0–100)",
     "AI回答に基づくブランド露出スコア（0〜100）",
     "AI Response-Based Brand Visibility Score (0–100)",
     "Y축 부제(점수 설명). axisAiAwareness('AI 호출도 →')/aiCallScoreTitle 축의 점수 라벨."),
    ("4분면 차트", "tooltip", "userInterest",
     USER_INTEREST_TOOLTIP_KR, USER_INTEREST_TOOLTIP_JP, USER_INTEREST_TOOLTIP_US,
     "CEP 관심도 i아이콘 호버 툴팁 본문. 전용 tooltip 네임스페이스. aiOptimizer.userInterestTitle 페어. node 1435-203214."),
    ("4분면 차트", "tooltip", "aiCallScore",
     AI_CALL_TOOLTIP_KR, AI_CALL_TOOLTIP_JP, AI_CALL_TOOLTIP_US,
     "AI 호출도 i아이콘 호버 툴팁 본문. 전용 tooltip 네임스페이스. aiOptimizer.aiCallScoreTitle 페어. node 1435-203214."),
]


def header():
    with TEMPLATE.open(encoding="utf-8") as f:
        return next(csv.reader(f))


def main():
    cols = header()
    ncol = len(cols)
    rows = [cols]

    def blank():
        return [""] * ncol

    for loc2, k1, k2, kr, jp, us, memo in NEW_ROWS:
        r = blank()
        r[0] = "AI 옵티마이저"   # 위치1
        r[1] = loc2             # 위치2
        r[2] = TODAY            # 작성일
        r[4] = memo             # 메모
        r[6] = k1               # key1
        r[7] = k2               # key2
        r[9] = kr               # KR
        r[10] = jp              # JP
        r[11] = us              # US
        rows.append(r)

    with OUT.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)

    print(f"wrote {OUT.name}: NEW={len(NEW_ROWS)} rows, cols={ncol}")


if __name__ == "__main__":
    main()
