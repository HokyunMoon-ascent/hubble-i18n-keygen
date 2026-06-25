# hubble-i18n-keygen

A [Claude Code](https://claude.com/claude-code) skill that generates new **KR / JP / US localization keys** for ListeningMind Hubble (AI Optimizer and friends).

Given a Figma screen or a description of new UI strings, it:

1. **Dedups** each candidate against the current `hubble_ko/ja/en-US.json` (and reuses existing translations).
2. **Names** keys by the existing convention — camelCase, `key1` namespace + `key2` identifier, sibling-feature mirroring (e.g. `cepFinder` → `aiOptimizer`), `Btn`/`Title`/`Label`/`Desc` suffixes.
3. **Translates** to Korean, Japanese, and English.
4. **Emits** a review-only `<feature>_keys.csv` in the project's 34-column sheet format.

## Why

Adding a localized feature to Hubble used to mean hand-repeating the same five steps and a near-identical `make_*_keys.py` script every time. This packages that process so it is consistent and fast.

## Install (as a Claude Code skill)

```bash
git clone https://github.com/HokyunMoon-ascent/hubble-i18n-keygen.git \
  ~/.claude/skills/hubble-i18n-keygen
```

Then invoke `/hubble-i18n-keygen` in Claude Code, or just hand it a Figma node + new strings.

## Layout

```
SKILL.md                     # skill definition + workflow
references/
  naming-guidelines.md       # naming rules (SSOT)
  sheet-format.md            # 34-column layout + column index map
scripts/
  make_keys.py               # spec JSON  ->  <feature>_keys.csv
  check_existing.py          # dedup / translation-reuse lookup
examples/
  axis_legend_spec.json      # a real worked spec
  make_axis_legend_keys.py   # the original one-off script it generalizes
```

## Manual use (without Claude)

```bash
# 1. dedup check
python3 scripts/check_existing.py --hubble-dir /path/to/json --kr "X축"

# 2. generate the CSV from a spec
python3 scripts/make_keys.py \
  --template /path/to/aiOptimizer_sheet.csv \
  --spec examples/axis_legend_spec.json \
  --out axis_legend_keys.csv \
  --loc1 "AI 옵티마이저" --date 2026-06-18
```

The generator reads the column header from `--template`, so the output always matches the master sheet's shape.
