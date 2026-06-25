---
name: hubble-i18n-keygen
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
description: Generate new KR/JP/US localization keys for ListeningMind Hubble / AI Optimizer features. Given a Figma screen (or a description of new UI strings), it dedups against the current hubble_ko/ja/en JSON, mirrors the existing naming conventions (camelCase, key1 namespace + key2 identifier, cepFinder→aiOptimizer pattern, Btn/Title/Label/Desc suffixes), translates to Korean/Japanese/English, and emits a review-only `<feature>_keys.csv` in the 34-column sheet format. Invoke when the user asks to "키 생성/추가", "make keys from this Figma", "다국어 키 csv", "hubble 키", "옵티마이저 키", or hands over a Figma node + new strings to localize.
---

# hubble-i18n-keygen

ListeningMind Hubble(AI 옵티마이저 등) 기능의 **신규 다국어(KR/JP/US) 로컬라이즈 키**를 만든다.
입력은 Figma 화면 + 신규 문자열, 출력은 기존 시트와 동일한 34열 포맷의 **검수 전용 `<feature>_keys.csv`** 다.

## Trigger
`/hubble-i18n-keygen` 또는 "이 Figma 보고 키 만들어줘 / hubble 키 추가 / 다국어 키 csv".

## 핵심 원칙
- **내용 불변**: 원문 의미·수치·고유명사를 바꾸지 않는다. 키 이름과 3개 언어 번역만 만든다.
- **기존 우선**: 이미 있는 키/문구는 새로 만들지 않는다. 중복은 제외하고 사유를 `삭제무방 및 비고`에 남긴다.
- **컨벤션 미러링**: 형제 기능(cepFinder 등)의 네이밍을 그대로 따라간다. (`references/naming-guidelines.md`)
- **신규만 분리**: 산출 CSV에는 이번에 만든 키만 담아 따로 검수할 수 있게 한다.

## 워크플로

### 0) 입력 확인
다음을 확보한다(없으면 사용자에게 질문):
- Figma node URL(들) 또는 신규 문자열 목록 + 각 문자열의 **컴포넌트 유형**(버튼/타이틀/라벨/툴팁/안내문)과 **소속 화면/카테고리**.
- baseline 현행 JSON: `hubble_ko-KR.json`, `hubble_ja-JP.json`, `hubble_en-US.json` 경로.
- 헤더 템플릿 CSV: `aiOptimizer_sheet.csv` (34열). 위치1 기본값(예: "AI 옵티마이저")과 작성일(YYYY-MM-DD).

> Figma node는 Figma MCP(`get_design_context`/`get_screenshot`)로 화면을 읽어 문자열·컴포넌트 유형을 파악할 수 있다. 화면이 없으면 사용자가 준 문자열·메모만으로 진행한다.

### 1) 중복 검사 (재사용 우선)
각 후보 문자열을 현행 JSON과 대조한다:
```
python3 scripts/check_existing.py --hubble-dir <dir> --kr "후보 한국어 문구" [--kr ...]
# 또는 키 충돌 확인:
python3 scripts/check_existing.py --hubble-dir <dir> --key aiOptimizer.userInterestTitle
```
- 동일/유사 문구가 이미 있으면 → **제외**, `삭제무방 및 비고`에 "기존 `<key1.key2>` 와 중복" 사유 기록.
- 기존 번역(JP/US)이 있으면 → 그대로 **재사용**.

### 2) 키 네이밍
`references/naming-guidelines.md` 를 따른다:
- camelCase. `key1` = 페이지/컴포넌트 네임스페이스(`label`, `tooltip`, `plan`, `aiOptimizer` …), `key2` = 식별자.
- 접미어: `Btn`/`Title`/`SubTitle`/`Notice`/`Guide`/`Desc`/`Label`. 접두어: `helptext`/`goTo`/동사 원형.
- 형제 기능 미러링: 예) `plan.tablecepFinder*` → `plan.tableaiOptimizer*`. 공용 라벨(X축/Y축)은 `label` 네임스페이스.

### 3) 번역
KR/JP/US 3종을 모두 작성한다. 멀티라인 툴팁은 `\n` 보존(`references/sheet-format.md` 인용 규칙 참고).

### 4) CSV 생성
키 스펙을 JSON으로 작성(`examples/axis_legend_spec.json` 형식)한 뒤:
```
python3 scripts/make_keys.py \
  --template <aiOptimizer_sheet.csv> \
  --spec <feature>_spec.json \
  --out <feature>_keys.csv \
  --loc1 "AI 옵티마이저" --date 2026-06-25
```
헤더는 템플릿에서 읽어 34열을 그대로 미러링한다. 컬럼 배치는 `references/sheet-format.md` 참고.

### 5) 검수
산출 CSV의 행 수·키·번역을 사용자에게 요약 제시하고, 제외된 중복 키와 사유도 함께 보고한다.

## 참고 파일
- `references/naming-guidelines.md` — 네이밍 룰 SSOT
- `references/sheet-format.md` — 34열 레이아웃 + 컬럼 인덱스 맵
- `examples/axis_legend_spec.json`, `examples/make_axis_legend_keys.py` — 실제 워크드 예시
