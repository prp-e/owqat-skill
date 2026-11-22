# owqat-skill

A Codex skill that looks up local prayer times and builds a bilingual Persian and English HTML card. The card highlights sunrise and sunset separately from the prayer times and shows the date in the Solar Hijri, Gregorian, and lunar Hijri calendars.

## Install

You need Codex with web access and Python 3. Clone this repository, then copy the skill and its supporting files into your Codex skills directory.

```sh
git clone https://github.com/prp-e/owqat-skill.git
skill_dir="${CODEX_HOME:-$HOME/.codex}/skills/owqat-skill"
mkdir -p "$skill_dir"
cp -R owqat-skill/SKILL.md owqat-skill/assets owqat-skill/scripts "$skill_dir/"
```

## Use

In a new Codex chat, enter a city name in Persian or English.

```text
$owqat-skill مشهد
$owqat-skill Tehran
```

The skill uses the city's local date by default. You can also request a specific date. Codex checks the source for the requested day and returns a standalone HTML file that opens in a browser.

The card shows Fajr, sunrise, Dhuhr, sunset, and Maghrib in local 24-hour time. Asr, Isha, and religious midnight appear when available. The card links to its sources and identifies the lunar calendar or provider used, since lunar dates can differ by a day.

## Files

- [SKILL.md](SKILL.md) defines the lookup and sourcing workflow.
- [assets/card.html](assets/card.html) is the responsive, bilingual template.
- [scripts/render.py](scripts/render.py) converts sourced JSON into a standalone HTML card using the Python standard library.
