"""Render a bilingual prayer timetable from verified source data."""
import argparse
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

EVENTS = {
    "fajr": ("اذان صبح", "Fajr"),
    "sunrise": ("طلوع آفتاب", "Sunrise"),
    "dhuhr": ("اذان ظهر", "Dhuhr"),
    "asr": ("عصر", "Asr"),
    "sunset": ("غروب آفتاب", "Sunset"),
    "maghrib": ("اذان مغرب", "Maghrib"),
    "isha": ("عشاء", "Isha"),
    "midnight": ("نیمه‌شب شرعی", "Religious midnight"),
}
DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def localized(fields, language):
    return escape(fields.get(language) or "—")


def render(data, template):
    values = {
        f"{field}_{language}": localized(data.get(field, {}), language)
        for field in ("city", "solar", "gregorian", "lunar")
        for language in ("fa", "en")
    }
    rows = {"fa": [], "en": []}
    for event, (fa, en) in EVENTS.items():
        time = data["times"].get(event) or "—"
        if time == "—" and event in {"asr", "isha", "midnight"}:
            continue
        if time != "—" and not re.fullmatch(r"(?:[01][0-9]|2[0-3]):[0-5][0-9]", time):
            raise ValueError(f"{event} requires a local time in HH:MM format")
        tile_class = "tile solar" if event in {"sunrise", "sunset"} else "tile"
        for language, label in (("fa", fa), ("en", en)):
            digits = time.translate(DIGITS) if language == "fa" else time
            rows[language].append(
                f'<div class="{tile_class}"><dt>{label}</dt>'
                f'<dd dir="ltr">{digits}</dd></div>'
            )
    sources = {"fa": [], "en": []}
    for source in data["sources"]:
        url = urlsplit(source["url"])
        if url.scheme not in {"http", "https"} or not url.hostname:
            raise ValueError("Sources require HTTP or HTTPS URLs")
        href = escape(url.geturl())
        for language in sources:
            label = localized(source["label"], language)
            sources[language].append(f'<li><a href="{href}">{label}</a></li>')
    for language in rows:
        values[f"events_{language}"] = "\n".join(rows[language])
        values[f"sources_{language}"] = "\n".join(sources[language])
        note = data.get("note", {}).get(language)
        values[f"note_{language}"] = f"<p>{escape(note)}</p>" if note else ""
    return re.sub(r"\{\{(\w+)\}\}", lambda match: values[match[1]], template)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    template = Path(__file__).resolve().parents[1] / "assets/card.html"
    data = json.loads(args.data.read_text(encoding="utf-8"))
    args.output.write_text(render(data, template.read_text(encoding="utf-8")), encoding="utf-8")
